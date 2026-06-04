import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Manual Tree Irrigation Calculator",
    layout="wide"
)

st.title("🚛 Manual Tree Irrigation Cost Calculator")
st.markdown("""
This application calculates the operational capacity and total costs of manually irrigating trees
using water tanks mounted on trucks.
""")

# =========================================================
# INPUT SECTION
# =========================================================

st.header("Input Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Field Parameters")

    tree_spacing = st.slider(
        "Tree Spacing (m)",
        min_value=3.0,
        max_value=6.0,
        value=4.0,
        step=0.1
    )

    row_spacing = st.slider(
        "Row Spacing (m)",
        min_value=3.0,
        max_value=6.0,
        value=4.0,
        step=0.1
    )

    tree_water_requirement = st.number_input(
        "Tree Water Requirement (L/day)",
        min_value=0.001,
        max_value=1000.0,
        value=20.0,
        step=0.1,
        format="%.3f"
    )

    irrigation_time_per_tree = st.slider(
        "Irrigation Time per Tree (minutes)",
        min_value=0.0,
        max_value=5.0,
        value=0.5,
        step=0.1
    )

with col2:
    st.subheader("Truck & Tank Parameters")

    tank_volume = st.slider(
        "Water Tank Volume (L)",
        min_value=1000,
        max_value=5000,
        value=3000,
        step=100
    )

    distance_to_water_source = st.number_input(
        "Distance from Water Source to Trees (m)",
        min_value=10.0,
        max_value=50000.0,
        value=5000.0,
        step=100.0
    )

    truck_speed = st.number_input(
        "Truck Speed (km/h)",
        min_value=1.0,
        max_value=120.0,
        value=40.0,
        step=1.0
    )

    fuel_consumption_truck = st.number_input(
        "Truck Fuel Consumption (L/km)",
        min_value=0.01,
        max_value=5.0,
        value=0.25,
        step=0.01
    )

    number_of_trucks = st.number_input(
        "Number of Trucks",
        min_value=1,
        max_value=100,
        value=1,
        step=1
    )

with col3:
    st.subheader("Operational Costs")

    daily_working_hours = st.slider(
        "Daily Working Hours",
        min_value=1,
        max_value=12,
        value=8,
        step=1
    )

    number_of_labor = st.number_input(
        "Number of Labor per Truck",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )

    pump_fuel_consumption = st.number_input(
        "Pump Fuel Consumption (L/h)",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        step=0.1
    )

    fuel_cost = st.number_input(
        "Fuel Cost ($/L)",
        min_value=0.0,
        max_value=10.0,
        value=1.0,
        step=0.01
    )

    water_cost = st.number_input(
        "Water Cost ($/m³)",
        min_value=0.0,
        max_value=1000.0,
        value=2.0,
        step=0.1
    )

    labor_cost = st.number_input(
        "Labor Cost ($/h per labor)",
        min_value=0.0,
        max_value=1000.0,
        value=10.0,
        step=1.0
    )

    truck_rent_cost = st.number_input(
        "Truck Rent Cost ($/day per truck)",
        min_value=0.0,
        max_value=10000.0,
        value=100.0,
        step=10.0
    )

# =========================================================
# CALCULATIONS
# =========================================================

st.header("Calculated Results")

# Total irrigation time available
total_available_time_hours = daily_working_hours * number_of_trucks

# Trees per tank
trees_per_tank = tank_volume / tree_water_requirement

# Irrigation time per tank
irrigation_time_per_tank_hours = (
    trees_per_tank * irrigation_time_per_tree
) / 60.0

# Pump discharge rate
if irrigation_time_per_tree > 0:
    required_pump_discharge = (
        tree_water_requirement / irrigation_time_per_tree
    )
else:
    required_pump_discharge = 0

# Travel time
distance_km = distance_to_water_source / 1000.0

round_trip_distance = distance_km * 2

travel_time_per_trip_hours = (
    round_trip_distance / truck_speed
)

# Refill time
# Assumed filling rate = 100 L/min
tank_refill_rate = 100.0  # L/min

refill_time_per_tank_hours = (
    tank_volume / tank_refill_rate
) / 60.0

# Total cycle time
cycle_time_hours = (
    irrigation_time_per_tank_hours
    + travel_time_per_trip_hours
    + refill_time_per_tank_hours
)

# Number of cycles/day
if cycle_time_hours > 0:
    cycles_per_day_per_truck = (
        daily_working_hours / cycle_time_hours
    )
else:
    cycles_per_day_per_truck = 0

# Total trees irrigated/day
total_trees_irrigated = (
    trees_per_tank
    * cycles_per_day_per_truck
    * number_of_trucks
)

# Actual operating times
actual_irrigation_time = (
    irrigation_time_per_tank_hours
    * cycles_per_day_per_truck
    * number_of_trucks
)

actual_refill_time = (
    refill_time_per_tank_hours
    * cycles_per_day_per_truck
    * number_of_trucks
)

actual_travel_time = (
    travel_time_per_trip_hours
    * cycles_per_day_per_truck
    * number_of_trucks
)

# Water used
total_water_used_liters = (
    total_trees_irrigated
    * tree_water_requirement
)

total_water_used_m3 = total_water_used_liters / 1000.0

# Fuel calculations
truck_fuel_used = (
    round_trip_distance
    * fuel_consumption_truck
    * cycles_per_day_per_truck
    * number_of_trucks
)

pump_fuel_used = (
    actual_irrigation_time
    * pump_fuel_consumption
)

total_fuel_used = truck_fuel_used + pump_fuel_used

total_fuel_cost = total_fuel_used * fuel_cost

# Labor cost
total_labor_cost = (
    number_of_labor
    * labor_cost
    * daily_working_hours
    * number_of_trucks
)

# Truck rent cost
total_truck_rent_cost = (
    truck_rent_cost
    * number_of_trucks
)

# Water cost
total_water_cost = (
    total_water_used_m3
    * water_cost
)

# Gross total cost
gross_total_cost = (
    total_fuel_cost
    + total_labor_cost
    + total_truck_rent_cost
    + total_water_cost
)

# =========================================================
# DISPLAY RESULTS
# =========================================================

res1, res2, res3 = st.columns(3)

with res1:
    st.metric(
        "Total Irrigated Trees per Day",
        f"{total_trees_irrigated:,.0f} trees/day"
    )

    st.metric(
        "Required Pump Discharge Rate",
        f"{required_pump_discharge:.2f} L/min"
    )

    st.metric(
        "Actual Irrigation Time",
        f"{actual_irrigation_time:.2f} h/day"
    )

with res2:
    st.metric(
        "Actual Tank Refill Time",
        f"{actual_refill_time:.2f} h/day"
    )

    st.metric(
        "Actual Traveling Time",
        f"{actual_travel_time:.2f} h/day"
    )

    st.metric(
        "Total Fuel Cost",
        f"${total_fuel_cost:,.2f}/day"
    )

with res3:
    st.metric(
        "Total Labor Cost",
        f"${total_labor_cost:,.2f}/day"
    )

    st.metric(
        "Total Truck Rent Cost",
        f"${total_truck_rent_cost:,.2f}/day"
    )

    st.metric(
        "Total Water Cost",
        f"${total_water_cost:,.2f}/day"
    )

st.subheader("Gross Total Daily Cost")

st.success(
    f"Gross Total Irrigation Cost = ${gross_total_cost:,.2f} per day"
)

# =========================================================
# DETAILED SUMMARY TABLE
# =========================================================

st.header("Detailed Summary")

summary_data = {
    "Parameter": [
        "Tree Spacing",
        "Row Spacing",
        "Tank Volume",
        "Tree Water Requirement",
        "Daily Working Hours",
        "Distance to Water Source",
        "Truck Speed",
        "Total Trees Irrigated",
        "Pump Discharge Rate",
        "Actual Irrigation Time",
        "Actual Refill Time",
        "Actual Traveling Time",
        "Fuel Cost",
        "Labor Cost",
        "Truck Rent Cost",
        "Water Cost",
        "Gross Total Cost"
    ],
    "Value": [
        tree_spacing,
        row_spacing,
        tank_volume,
        tree_water_requirement,
        daily_working_hours,
        distance_to_water_source,
        truck_speed,
        total_trees_irrigated,
        required_pump_discharge,
        actual_irrigation_time,
        actual_refill_time,
        actual_travel_time,
        total_fuel_cost,
        total_labor_cost,
        total_truck_rent_cost,
        total_water_cost,
        gross_total_cost
    ],
    "Unit": [
        "m",
        "m",
        "L",
        "L/day",
        "h/day",
        "m",
        "km/h",
        "trees/day",
        "L/min",
        "h/day",
        "h/day",
        "h/day",
        "$/day",
        "$/day",
        "$/day",
        "$/day",
        "$/day"
    ]
}

summary_df = pd.DataFrame(summary_data)

st.dataframe(summary_df, use_container_width=True)

# =========================================================
# EXPORT TO EXCEL
# =========================================================

def convert_df_to_excel(df):
    output_file = "manual_irrigation_results.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Results")

    return output_file

excel_file = convert_df_to_excel(summary_df)

with open(excel_file, "rb") as file:
    st.download_button(
        label="📥 Download Results as Excel",
        data=file,
        file_name=f"manual_irrigation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
