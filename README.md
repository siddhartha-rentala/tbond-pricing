## **Treasury Bond Pricing**

### **Project Overview:**
This project calculates present values and yields for Treasury bond holdings using daily Treasury rates. It also constructs a zero-coupon yield curve for accurate bond pricing.

### **Key Features:**
1. **Yield Curve Bootstrapping:** Constructs a zero-coupon curve from Treasury yields.
2. **Present Value Discounting:** Computes the present value of bonds using the risk-free discount rate.
3. **Interest Rate Sensitivity:** Analyzes bond prices under different rate scenarios.

### **Installation:**
```bash
pip install pandas numpy matplotlib
```

### **Usage:**
```bash
python TreasuryBondPricing.py
```

### **Results:**
1. **Yield Curve:** A line chart showing the bootstrapped yield curve.
2. **Bond Price Sensitivity:** A plot showing how bond prices change with interest rate movements.
