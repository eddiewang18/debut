from datetime import datetime, timedelta
import math
from scipy import stats

def get_date_minus_days(d):
    # 取得今天的日期
    today = datetime.now()
    # 減去指定的天數
    target_date = today - timedelta(days=d)
    # 格式化日期為 YYYY-mm-dd
    return target_date.strftime('%Y-%m-%d')

# t檢定
def t_test(x1_avg, x2_avg, n1, n2, s1, s2, alpha=0.05):
    # 計算t統計量
    pooled_std = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    t_stat = (x1_avg - x2_avg) / (pooled_std * math.sqrt(1/n1 + 1/n2))
    
    # 自由度
    df = n1 + n2 - 2
    
    # 臨界值 (雙尾檢定)
    critical_value = stats.t.ppf(1 - alpha / 2, df)
    
    # 判斷是否拒絕零假設
    reject_null = abs(t_stat) > critical_value
    
    return t_stat, critical_value, reject_null

# z檢定
def z_test(x1_avg, x2_avg, n1, n2, std, alpha=0.05):
    # 計算z統計量
    z_stat = (x1_avg - x2_avg) / (std * math.sqrt(1/n1 + 1/n2))
    
    # 臨界值 (雙尾檢定)
    critical_value = stats.norm.ppf(1 - alpha / 2)
    
    # 判斷是否拒絕零假設
    reject_null = abs(z_stat) > critical_value
    
    return z_stat, critical_value, reject_null