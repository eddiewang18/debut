from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import F
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
                # machine.machine_name = machine_data.get('machine_name', machine.machine_name)
                # machine.connecting_plate = machine_data.get('connecting_plate', machine.connecting_plate)
                # machine.machine_amt = machine_data.get('machine_amt', machine.machine_amt)
                # machine.save()
                serializer = MachineSerializer(machine, data=machine_data)
                if serializer.is_valid():
                    serializer.save()
                    machine_data = serializer.data
                else:
                    print("========================================>A")
                    return Response({
                        'errcode':1,
                        'msg': '新機器資料建立失敗'
                        }, status=400
                        )
                    # machine_data = serializer.data
                # return Response({
                #     'errcode':0,
                #     'msg': '機器資料更新成功'
                #     }, status=200
                #     )
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
                print("========================================>B")
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
            print(f"deleted_count===>{deleted_count}")
        print("========================================>C")
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