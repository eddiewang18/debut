from django.core.management.base import BaseCommand
from core.utils import get_date_minus_days
from ...models import *
import random
import traceback


class Command(BaseCommand):
    help = '這是一個用於建立日報測試資料的指令，'  

    def add_arguments(self, parser):
        # 定義指令的參數
        parser.add_argument('--day', type=int, help='建立近幾日的資料')

    def handle(self, *args, **kwargs):
        # 實作指令的邏輯
        self.stdout.write(f'開始建立測試資料 .....')
        try :
            Machine_line_record.objects.all().delete()
            machine_obj = Machine.objects.all()
            day = kwargs.get('day') if kwargs.get('day') else 60
            create_instances = []

            for obj in machine_obj :
                # machine_id = obj.machine_id
                line_obj = obj.lines.all()
                for line in line_obj:
                    # machine_line_id = line.machine_line_id
                    emp_default_amt = line.emp_default_amt if line.emp_default_amt else 0
                    for d in range(day,-1,-1):
                        production_day = get_date_minus_days(d)
                        create_instances.append(
                            Machine_line_record(
                                machine_id = obj,
                                machine_line_id = line,
                                production_day = production_day,
                                machine_line_amt = random.randint(100,500),
                                emp_amt = random.randint(1,emp_default_amt+3),
                                work_hours = random.randint(5,25),
                            )
                        )
            print(f"size of create_instances:{len(create_instances)}")
            if len(create_instances)>0:
                Machine_line_record.objects.bulk_create(create_instances)
                self.style.SUCCESS('成功建立測試資料')
        except Exception as e:
            traceback.print_exc()
        finally:
            self.stdout.write(f'程序結束')

        
