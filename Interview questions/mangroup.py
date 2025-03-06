def price():
    try:
        years_to_maturity = float(input().strip())
        face_value = float(input().strip())
        
        if years_to_maturity <= 0 or face_value <= 0:
            print("Error: invalid maturity/face value")
            return
        
        coupon_times_str = input().strip()
        coupon_amounts_str = input().strip()
        
        if not coupon_times_str or not coupon_amounts_str:
            print("Error: invalid input format")
            return
            
        coupon_times = [float(x.strip()) for x in coupon_times_str.split(',')]
        coupon_amounts = [float(x.strip()) for x in coupon_amounts_str.split(',')]
        
        discount_times_str = input().strip()
        discount_factors_str = input().strip()
        
        if not discount_times_str or not discount_factors_str:
            print("Error: invalid input format")
            return
            
        discount_times = [float(x.strip()) for x in discount_times_str.split(',')]
        discount_factors = [float(x.strip()) for x in discount_factors_str.split(',')]
        
        if len(coupon_times) != len(coupon_amounts):
            print("Error: invalid input format")
            return
            
        if len(discount_times) != len(discount_factors):
            print("Error: invalid input format")
            return
            
        for amount in coupon_amounts:
            if amount < 0:
                print("Error: invalid coupon schedule")
                return
                
        for factor in discount_factors:
            if factor < 0 or factor > 1:
                print("Error: invalid discount curve")
                return
                
        for i in range(1, len(coupon_times)):
            if coupon_times[i] <= coupon_times[i-1]:
                print("Error: invalid coupon schedule")
                return
                
        for i in range(1, len(discount_times)):
            if discount_times[i] <= discount_times[i-1]:
                print("Error: invalid discount curve")
                return
        
        total_pv = 0
        
        for time, amount in zip(coupon_times, coupon_amounts):
            if time < 0 or time > years_to_maturity:
                print("Error: invalid coupon schedule")
                return
                
            discount_factor = None
            for d_time, d_factor in zip(discount_times, discount_factors):
                if d_time <= time:
                    discount_factor = d_factor
            
            if discount_factor is None:
                print("Error: invalid discount curve")
                return
                
            total_pv += amount * discount_factor
            
        discount_factor = None
        for d_time, d_factor in zip(discount_times, discount_factors):
            if d_time <= years_to_maturity:
                discount_factor = d_factor
                
        if discount_factor is None:
            print("Error: invalid discount curve")
            return
            
        total_pv += face_value * discount_factor
        
        print(f"{total_pv:.2f}")
        
    except ValueError:
        print("Error: invalid input format")
    except Exception:
        print("Error: invalid input format")