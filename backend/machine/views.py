from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import F,Q, Avg, StdDev, FloatField , Subquery , OuterRef
from django.utils.timezone import now
import numpy as np

# from datetime import datetime


# Create your views here.

class MachineList(APIView):

    field_query_rules = {
        "machine_name":"machine_name__icontains"
    }

    def get(self, request, format=None):
        data_from_db = Machine.objects.all()
        queryParams = dict(request.query_params) 
        for queryParam,queryVal in queryParams.items():
            if queryVal and queryParam in MachineList.field_query_rules :
                queryVal = queryVal[0] 
                data_from_db = data_from_db.filter(**{MachineList.field_query_rules[queryParam]:queryVal})
                
                
        serializer = MachineSerializer(data_from_db, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # 取得請求的資料
        data = request.data         
        
        machine_data = data.get('machine')
        machine_id = machine_data.get("machine_id")
        machine_line_create_update = data.get('machine_line_create_update')
        machine_line_del = data.get("machine_line_del")
        # 檢查 machine_id 是否有值
        if machine_id:  # 有值 -> 更新
            try:
                # 查詢對應的機器
                machine = Machine.objects.get(machine_id=machine_id)
                # 更新資料

                serializer = MachineSerializer(machine, data=machine_data)
                if serializer.is_valid():
                    serializer.save()
                    machine_data = serializer.data
                else:
                    return Response({
                        'errcode':1,
                        'msg': '新機器資料建立失敗'
                        }, status=400
                        )
            except Machine.DoesNotExist:
                return Response({
                    'errcode':1,
                    'msg': '指定的機器不存在'
                    }, status=404
                    )
        else:  # 無值 -> 新增
            serializer = MachineSerializer(data=machine_data)
            if serializer.is_valid():
                serializer.save()
                machine_data = serializer.data
                machine_id = dict(machine_data)["machine_id"]
            else:
                return Response({
                    'errcode':1,
                    'msg': '新機器資料建立失敗'
                    }, status=400
                    )

        # 準備分類的資料
        update_instances = []
        create_instances = []
        machine_instance = Machine.objects.get(machine_id=machine_id)
        if len(machine_line_create_update) > 0 :
            # 遍歷資料
            for item in machine_line_create_update:
                machine_line_id = item.get('machine_line_id')

                if machine_line_id:  # 更新資料
                    try:
                        # 從資料庫中取得對應的物件
                        machine_line = Machine_line.objects.get(machine_line_id=machine_line_id)
                        machine_line.machine_id = machine_instance
                        machine_line.machine_line_name = item.get('machine_line_name', machine_line.machine_line_name)
                        machine_line.emp_default_amt = item.get('emp_default_amt', machine_line.emp_default_amt)
                        update_instances.append(machine_line)
                    except Machine_line.DoesNotExist:
                        # 如果找不到指定的資料，略過或記錄錯誤
                        continue
                else:  # 新增資料
                    create_instances.append(Machine_line(
                        machine_id=machine_instance,
                        machine_line_name=item.get('machine_line_name'),
                        emp_default_amt=item.get('emp_default_amt'),
                    ))

            # 使用 transaction 保持原子性
            with transaction.atomic():
                # 批量更新資料
                if update_instances:
                    Machine_line.objects.bulk_update(update_instances, [
                        'machine_line_name', 'emp_default_amt'
                    ])

                # 批量新增資料
                if create_instances:
                    Machine_line.objects.bulk_create(create_instances)

        # 處理線的刪除資料
        if len(machine_line_del)>0 :
            ids_to_del = [row['machine_line_id'] for row in machine_line_del]
            # 執行批量刪除
            deleted_count, _ = Machine_line.objects.filter(pk__in=ids_to_del).delete()
            # 回應成功訊息
        return Response({
            'errcode':0,
            'msg': '機器資料更新成功',
            "machine_data":machine_data
            }, status=200
            )

class MachineDetail(APIView):

    def get_object(self, pk):
        try:
            return Machine.objects.get(pk=pk)
        except Machine.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data_object = self.get_object(pk)
        serializer = MachineSerializer(data_object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        data_object = self.get_object(pk)
        data_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class Machine_line_record_view(APIView):

    def get(self,request,pk):
        result = {}
        queryParams = dict(request.query_params)
        production_day = queryParams.get("production_day")[0]
        machine_id = pk
        raw = True
        mdatetime = None
        
        # 判斷機種在某一日是否有各線別的資料
        
        data = Machine_line_record.objects.filter(Q(machine_id=machine_id) & Q(production_day=production_day))
        machine_obj = list(Machine.objects.filter(pk=machine_id).values("machine_id","machine_name","connecting_plate","machine_amt"))
        if data.count() > 0:
            raw = False
            machine_line_record_data = list(Machine_line_record.objects.filter(
                                            machine_id=machine_id,  # 假設 machine_id 是主鍵或唯一的字段，直接比較
                                            production_day=production_day
                                        ).select_related('machine_line_id').annotate(
                                            machine_line_name=F('machine_line_id__machine_line_name')
                                        ).values('record_id','machine_line_id', 'machine_line_name','production_day','machine_line_amt','emp_amt','work_hours','overhead_wire','ng',"mdatetime"))
            result = machine_obj[0]
            result['machine_lines'] = []
            for row in machine_line_record_data:
                result['machine_lines'].append(row)                 
            mdatetime = str(machine_line_record_data[0]['mdatetime'])[:19]
            print(f"mdatetime=>{mdatetime}")
        else :
            
            machine_line_obj = list(Machine_line.objects.filter(machine_id = machine_id).values("machine_line_id","machine_line_name","emp_default_amt"))
            # print(f"machine_obj:{machine_obj}\n\nmachine_line_obj:{machine_line_obj}\n\n")
            result = machine_obj[0]
            result['machine_lines'] = []
            for row in machine_line_obj:
                row['production_day']=production_day
                row['machine_line_amt']=0
                row['emp_amt']=row['emp_default_amt']
                del row['emp_default_amt']
                row['work_hours'] = 10
                row['overhead_wire'] = ''
                row['ng'] = ''
                result['machine_lines'].append(row)
        """
            {
                machine_id:xxx,
                machine_name:xxx,
                connecting_plate:xxx,
                machine_amt:xxx,
                machine_lines:[
                    {'machine_line_id': 6, 'machine_line_name': 'A', 'emp_default_amt': 4,production_day:'',machine_line_amt:0,emp_amt:emp_default_amt,work_hours:10,overhead_wire:'',ng:''}, 
                    {'machine_line_id': 7, 'machine_line_name': 'B', 'emp_default_amt': 2,production_day:'',machine_line_amt:0,emp_amt:emp_default_amt,work_hours:10,overhead_wire:'',ng:''}
                    
                ]
            }
        """
        return Response({"result":result,"raw":raw,"mdatetime":mdatetime})

class Machine_line_record_create(APIView):
    def get_object(self, pk):
        try:
            return Machine_line_record.objects.get(pk=pk)
        except Machine_line_record.DoesNotExist:
            raise Http404
    def post(self,request):
        serializer  = Machine_line_record_Serializer(data=request.data,many=True)
        raw = True
        mdatetime = None
        if serializer.is_valid():
            serializer.save()
            save_data = list(serializer.data)
            machine_id = save_data[0]['machine_id']
            machine_obj = list(Machine.objects.filter(pk=machine_id).values("machine_id","machine_name","connecting_plate","machine_amt"))

            machine_line_record_data = list(Machine_line_record.objects.filter(
                                            machine_id=machine_id,  # 假設 machine_id 是主鍵或唯一的字段，直接比較
                                            production_day=save_data[0]['production_day']
                                        ).select_related('machine_line_id').annotate(
                                            machine_line_name=F('machine_line_id__machine_line_name')
                                        ).values('record_id','machine_line_id', 'machine_line_name','production_day','machine_line_amt','emp_amt','work_hours','overhead_wire','ng',"mdatetime"))
            result = machine_obj[0]
            result['machine_lines'] = []
            mdatetime = str(machine_line_record_data[0]['mdatetime'])[:19]
            for row in machine_line_record_data:
                result['machine_lines'].append(row)                 

            raw = False

            return Response(
                {"result":result,"raw":raw,'errcode':0,'msg': '日報資料新建成功',"mdatetime":mdatetime}, 
                status=201
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        objects = []
        for row in request.data:
            obj = self.get_object(row['record_id'])
            for field , val in row.items():
                if field not in ['record_id','machine_line_id','machine_id']:
                    setattr(obj,field,val)
            obj.mdatetime = now()
            objects.append(obj)

        try:
            Machine_line_record.objects.bulk_update(objects, fields=['machine_line_amt', 'emp_amt', 'work_hours','overhead_wire','ng','mdatetime'])
            
            machine_id =  request.data[0]['machine_id']
            production_day = request.data[0]['production_day']
            machine_obj = list(Machine.objects.filter(pk=machine_id).values("machine_id","machine_name","connecting_plate","machine_amt"))
            result = machine_obj[0]
            result['machine_lines'] = []

            machine_line_record_data = list(Machine_line_record.objects.filter(
                                            machine_id=machine_id,  # 假設 machine_id 是主鍵或唯一的字段，直接比較
                                            production_day=production_day
                                        ).select_related('machine_line_id').annotate(
                                            machine_line_name=F('machine_line_id__machine_line_name')
                                        ).values('record_id','machine_line_id', 'machine_line_name','production_day','machine_line_amt','emp_amt','work_hours','overhead_wire','ng',"mdatetime"))

            mdatetime = str(machine_line_record_data[0]['mdatetime'])[:19]
            print(f"\nsize of {production_day} record ==> {len(machine_line_record_data)}\n")
            for row in machine_line_record_data:
                result['machine_lines'].append(row)  
            
            return Response({
                'errcode':0,
                'msg': '日報資料更新成功',
                "result":result,
                "mdatetime":mdatetime
                }, status=200
                )
        except Exception as e :
            print(f"error===>\n{e}\n")
            return Response({
                'errcode':1,
                'msg': '日報資料更新失敗'
                }, status=400
                )

class Machine_stat1(APIView):
    def get(self,request):
        raw_data = list(Machine_line_record.objects.all().values("machine_line_amt","emp_amt","work_hours"))

        tmp_ary = {
            "machine_line_amt":[],
            "emp_amt":[],
            "tot_work_hours":[]
        }

        response = []
        machine_line_amt = []
        emp_amt = []
        tot_work_hours = []

        for row in raw_data :
            machine_line_amt.append(row['machine_line_amt'])
            emp_amt.append(row['emp_amt'])
            tot_work_hours.append(row['work_hours']*row['emp_amt'])


        tmp_ary['machine_line_amt'] = [
            {
                "x":'整體數量平均數',
                "y":round(sum(machine_line_amt)/len(machine_line_amt),2)
            },
            {
                "x":'整體數量中位數',
                "y":round(np.median(machine_line_amt),2)
            },
            {
                "x":'整體數量標準差',
                "y":round(np.std(machine_line_amt),2)
            }
        ]

        tmp_ary['emp_amt'] = [
            {
                "x":'員工數量平均數',
                "y":round(sum(emp_amt)/len(emp_amt),2)
            },
            {
                "x":'員工數量中位數',
                "y":round(np.median(emp_amt),2)
            },
            {
                "x":'員工數量標準差',
                "y":round(np.std(emp_amt),2)     
            }
        ]     

        tmp_ary['tot_work_hours'] = [
            {
                "x":'總工時平均數',
                "y":round(sum(tot_work_hours)/len(tot_work_hours),2)
            },
            {
                "x":'總工時中位數',
                "y":round(np.median(tot_work_hours),2)
            },
            {
                "x":'總工時標準差',
                "y":round(np.std(tot_work_hours),2)    
            }
        ] 
        
        return Response(tmp_ary)

class Machine_stat2(APIView):

    # def get(self,request):

    #     # 聚合查詢
    #     result = (
    #         Machine_line_record.objects.values(machine_name=F('machine_id__machine_name'))
    #         .annotate(
    #             avg_machine_line_amt=Avg('machine_line_amt', output_field=FloatField()),
    #             avg_emp_amt=Avg('emp_amt', output_field=FloatField()),
    #             avg_work_hours=Avg('work_hours', output_field=FloatField()),
    #             avg_emp_work_hours=Avg(F('emp_amt') * F('work_hours'), output_field=FloatField()),
    #             stddev_machine_line_amt=StdDev('machine_line_amt', sample=False, output_field=FloatField()),
    #             stddev_emp_amt=StdDev('emp_amt', sample=False, output_field=FloatField()),
    #             stddev_work_hours=StdDev('work_hours', sample=False, output_field=FloatField()),
    #             stddev_emp_work_hours=StdDev(F('emp_amt') * F('work_hours'), sample=False, output_field=FloatField()),
    #         )
    #         .order_by('-machine_name')  # 降序排列
    #     )

    #     for row in result:
    #         for k,v in row.items() :
    #             try :
    #                 row[k] = round(v,2)
    #             except TypeError :
    #                 pass
    #     # print(f"Machine_stat2 result=>\n{result}\n")
    #     return Response(result)

    def get(self,request):

        result = {}

        grp_dict = {}

        series = []

        data = list(Machine_line_record.objects.all().values(
            "machine_line_amt",
            "emp_amt",
            "work_hours",
            tot_work_hours = F("emp_amt")*F("work_hours"),
            machine_name=F('machine_id__machine_name')
            )
        )
        for row in data :
            if row['machine_name'] not in grp_dict :
                grp_dict[row['machine_name']] = {
                    "machine_line_amt":[],
                    "emp_amt":[],
                    "work_hours":[],
                    "tot_work_hours":[]
                }
            
            for k,v in row.items():
                if k != 'machine_name':
                    grp_dict[row['machine_name']][k].append(v)

        result['categories'] = list(grp_dict.keys())

        result['machine_line_amt'] = {
            "avg":[],
            "median":[],
            "std":[]
        }

        result['emp_amt'] = {
            "avg":[],
            "median":[],
            "std":[]
        }

        result['work_hours'] = {
            "avg":[],
            "median":[],
            "std":[]
        }

        result['tot_work_hours'] = {
            "avg":[],
            "median":[],
            "std":[]
        }

        for k,v in grp_dict.items() :
            for field , ary in v.items():
                avg = round(sum(ary)/len(ary),2)
                median = round(np.median(ary),2)
                std = round(np.std(ary),2)   
                result[field]['avg'].append(avg)
                result[field]['median'].append(median)
                result[field]['std'].append(std)


        return Response(result)