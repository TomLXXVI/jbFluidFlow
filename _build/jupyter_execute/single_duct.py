#!/usr/bin/env python
# coding: utf-8

# # Air Flow through a Duct
# ---

# In this notebook it is shown how to size a single air duct using the package `fluid_flow` which is part of the main package `hvac`.

# In[1]:


from deps import load_packages
load_packages()


# In[2]:


import jupyter_addons as ja
ja.set_css()


# ## Let's Import What We'll Need

# In[3]:


from hvac import Quantity
from hvac.fluid_flow import Duct, Rectangular
from hvac.fluids import Fluid


# We define a shortcut for instantiating `Quantity` objects:

# In[4]:


Q_ = Quantity


# ## Define Standard Dry Air

# We use standard dry air for sizing the duct. The code below shows how standard air is defined. 

# In[5]:


Air = Fluid('Air')
STANDARD_AIR = Air(T=Q_(20, 'degC'), P=Q_(101_325, 'Pa'))


# ## Sizing a Rectangular Duct

# A duct has a cross-section. Three types of cross-section are available:
# - circular
# - rectangular
# - flat-oval
# 
# Here we will size a rectangular duct. The height of the rectangular cross-section must be known beforehand. The width will then be calculated. To create a rectangular cross-section with a height of 100 mm, we write:

# In[6]:


cross_section = Rectangular.create(height=Q_(100, 'mm'))


# The required width of the duct will depend on the design volume flow rate through the duct and the selected specific pressure drop (i.e. per unit of duct length). To size a duct we need to specify:
# - the length of the duct
# - wall roughness (for a galvanized steel duct with medium roughness this is 0.09 mm)
# - the fluid that flows through the duct (in this case standard air as defined above)
# - the cross-section (of which the required width needs to be determined)
# - the volume flow rate of the fluid through the duct
# - either the specific pressure drop or the total pressure drop across the straight length of duct; in this example a specific pressure drop will be specified.

# In[7]:


duct = Duct.create(
    length=Q_(18.2, 'm'),
    wall_roughness=Q_(0.09, 'mm'),
    fluid=STANDARD_AIR,
    cross_section=cross_section,
    volume_flow_rate=Q_(500, 'm ** 3 / hr'),
    specific_pressure_drop=Q_(1.28, 'Pa / m')
)


# Once the duct is created with the parameters above, we can retrieve the required width of the duct's cross-section through the `cross_section` property of the `Duct` object:

# In[8]:


ja.display_list([
    f"cross-section width of duct: <b>{duct.cross_section.width.to('mm'):~P.3f}</b>"
])


# The equivalent diameter, hydraulic diameter, and the cross-section area of the duct can also be requested:

# In[9]:


ja.display_list([
    f"equivalent diameter: <b>{duct.cross_section.equivalent_diameter.to('mm'):~P.3f}</b>",
    f"hydraulic diameter: <b>{duct.cross_section.hydraulic_diameter.to('mm'):~P.3f}</b>",
    f"cross-section area: <b>{duct.cross_section.area.to('cm ** 2'):~P.3f}</b>"
])


# The total (friction) pressure drop over the whole length of duct can be attained by:

# In[10]:


ja.display_list([
    f"pressure drop: <b>{duct.pressure_drop.to('Pa'):~P.3f}</b>"
])


# ### Sizing a Rectangular Duct with a Schedule

# In order to get a cross-section of the duct which is commercially available, we will couple a "schedule" (an instance of the `DuctSchedule` class) with the cross-section. For rectangular ducts a default schedule is available:

# In[11]:


from hvac.fluid_flow import rectangular_duct_schedule


# To indicate that we want the nearest commercially available width, we add the parameter `schedule` when creating the cross-section:

# In[12]:


cross_section = Rectangular.create(height=Q_(100, 'mm'), schedule=rectangular_duct_schedule)


# Now we create the duct like before:

# In[13]:


duct = Duct.create(
    length=Q_(18.2, 'm'),
    wall_roughness=Q_(0.09, 'mm'),
    fluid=STANDARD_AIR,
    cross_section=cross_section,
    volume_flow_rate=Q_(500, 'm ** 3 / hr'),
    specific_pressure_drop=Q_(1.28, 'Pa / m')
)


# In[14]:


ja.display_list([
    f"cross-section width of duct: <b>{duct.cross_section.width.to('mm'):~P.1f}</b>"
])


# In[15]:


ja.display_list([
    f"equivalent diameter: <b>{duct.cross_section.equivalent_diameter.to('mm'):~P.3f}</b>",
    f"hydraulic diameter: <b>{duct.cross_section.hydraulic_diameter.to('mm'):~P.3f}</b>",
    f"cross-section area: <b>{duct.cross_section.area.to('cm ** 2'):~P.3f}</b>"
])


# As the commercially available width is different from the calculated value, the specific pressure drop that we've initially specified won't be valid anymore:

# In[16]:


ja.display_list([
    f"specific pressure drop across duct: <b>{duct.specific_pressure_drop.to('Pa / m'):~P.3f}</b>",
    f"pressure drop across duct: <b>{duct.pressure_drop.to('Pa'):~P.3f}</b>"
])


# Other flow quantities that can be retrieved after the duct has been created, are:

# In[17]:


ja.display_list([
    f"the air velocity in the duct: <b>{duct.velocity.to('m / s'):~P.3f}</b>",
    f"the reynolds number: <b>{duct.reynolds_number:.3f}</b>",
    f"the velocity pressure: <b>{duct.velocity_pressure:~P.3f}</b>"
])


# ## Air Volume Flow Rate through a Rectangular Duct

# Let's keep the duct from the example above. Suppose that a pressure drop of 50 Pa exists along the duct. The question is now what air volume flow rate is causing this pressure drop.

# In[18]:


duct.pressure_drop = Q_(50, 'Pa')


# In[19]:


ja.display_list([
    f"volume flow rate through duct = <b>{duct.volume_flow_rate.to('m ** 3 / hr'):~P.1f}</b>"
])


# ## Sizing a Circular Duct

# When sizing a circular duct for a given design volume flow rate and pressure drop, the only thing we know is that the duct has a circular cross-section. A circular cross-section is represented by the `Circular` class.

# In[20]:


from hvac.fluid_flow import Circular


# Simply call `create` on the `Circular` class to create the cross-section:

# In[21]:


cross_section = Circular.create()


# Using the same design values as for the rectangular duct above, we create the circular duct in exactly the same way:

# In[22]:


duct = Duct.create(
    length=Q_(18.2, 'm'),
    wall_roughness=Q_(0.09, 'mm'),
    fluid=STANDARD_AIR,
    cross_section=cross_section,
    volume_flow_rate=Q_(500, 'm ** 3 / hr'),
    specific_pressure_drop=Q_(1.28, 'Pa / m')
)


# To get at the required internal diameter to establish the requested specific pressure drop at the design volume flow rate, we write: 

# In[23]:


ja.display_list([
    f"cross-section internal diameter: <b>{duct.cross_section.internal_diameter.to('mm'):~P.3f}</b>"
])


# A circular cross-section also has the equivalent and hydraulic diameter being defined; obviously they are equal to the internal diameter.

# In[24]:


ja.display_list([
    f"equivalent diameter: <b>{duct.cross_section.equivalent_diameter.to('mm'):~P.3f}</b>",
    f"hydraulic diameter: <b>{duct.cross_section.hydraulic_diameter.to('mm'):~P.3f}</b>",
    f"cross-section area: <b>{duct.cross_section.area.to('cm ** 2'):~P.3f}</b>"
])


# As the length of the circular duct is the same as that of the rectangular duct, and as we have used the same specific pressure drop, the total pressure drop along the circular duct should be equal to the total pressure drop along the rectangular duct: 

# In[25]:


ja.display_list([
    f"pressure drop: <b>{duct.pressure_drop.to('Pa'):~P.3f}</b>"
])


# > Notice that the equivalent diameter of the rectangular duct in the previous example matches with the internal diameter of the circular duct.

# ### Sizing a Circular Duct with a Schedule

# In the same way as for the rectangular duct, we can assign a "schedule" to the cross-section of a circular duct in order to retrieve an internal diameter of the duct that is commercially available.

# In[26]:


from hvac.fluid_flow import circular_duct_schedule


# In[27]:


cross_section = Circular.create(schedule=circular_duct_schedule)

duct = Duct.create(
    length=Q_(18.2, 'm'),
    wall_roughness=Q_(0.09, 'mm'),
    fluid=STANDARD_AIR,
    cross_section=cross_section,
    volume_flow_rate=Q_(500, 'm ** 3 / hr'),
    specific_pressure_drop=Q_(1.28, 'Pa / m')
)

ja.display_list([
    f"cross-section internal diameter: <b>{duct.cross_section.internal_diameter.to('mm'):~P.3f}</b>"
])


# In[28]:


ja.display_list([
    f"specific pressure drop across duct: <b>{duct.specific_pressure_drop.to('Pa / m'):~P.3f}</b>",
    f"pressure drop across duct: <b>{duct.pressure_drop.to('Pa'):~P.3f}</b>"
])


# ### Replace a Circular Duct by an Equivalent Rectangular Duct

# Assume that we need to replace this circular duct by a rectangular duct while keeping the pressure drop the same. To accomplish this, we can create a rectangular cross-section of which the equivalent diameter is equal to the internal diameter of the circular duct. The height of the rectangular duct we can choose ourselves, but the width still needs to be calculated.

# In[29]:


rect_cross_sect = Rectangular.create(height=Q_(100, 'mm'), equivalent_diameter=cross_section.internal_diameter)

ja.display_list([
    f"width of the equivalent rectangular duct: <b>{rect_cross_sect.width.to('mm'):~P.3f}</b>"
])


# Let's check if we still have the same pressure drop. Therefore, we create a rectangular duct with the same length and with the same air volume flow rate as the circular duct. When we create the rectangular duct, we don't know the specific pressure drop nor the total pressure drop, as this is just what we are looking for. So we omit these parameters when instantiating the duct. The program will notice that the cross-section of the duct is fully determined and that the volume flow rate is given, so it deduces that it is pressure drop that needs to be calculated. 

# In[30]:


rect_duct = Duct.create(
    length=Q_(18.2, 'm'),
    wall_roughness=Q_(0.09, 'mm'),
    fluid=STANDARD_AIR,
    cross_section=rect_cross_sect,
    volume_flow_rate=Q_(500, 'm ** 3 / hr')
)


# In[31]:


ja.display_list([
    f"specific pressure drop across duct: <b>{rect_duct.specific_pressure_drop.to('Pa / m'):~P.3f}</b>",
    f"pressure drop across duct: <b>{rect_duct.pressure_drop.to('Pa'):~P.3f}</b>"
])


# ## Sizing a Flat-Oval Duct

# Sizing a flat-oval duct is similar to sizing a rectangular duct. Instead of `Rectangular` instantiate the cross-section from class `FlatOval`. The corresponding default schedule is now `flat_oval_duct_schedule`.

# ## Adding a Fitting to a Rectangular Duct

# We will add a rectangular, mitered elbow to our last created rectangular duct. The loss coefficients of duct fittings are calculated based on the fitting loss coefficient tables in **SMACNA’s handbook “HVAC SYSTEMS - DUCT DESIGN”, Fourth Edition (2006)**. The designation of the fittings available in the program corresponds with the designation of the fitting loss tables in the handbook. The loss coefficients of rectangular mitered elbows can be found in table A-7,D of SMACNA’s handbook. For a complete overview of all the available duct fittings see the file `smacna.py` in the subpackage `fluid_flow.fittings.duct`.
# 
# Adding a fitting to a duct is a two-step process. First create the fitting object, and then add it to the duct.

# **Create the Fitting**

# In[32]:


from hvac.fluid_flow.fittings.duct import ElbowA7D


# In[33]:


elbow = ElbowA7D(ID='elbow1', duct=rect_duct, theta=Q_(90, 'deg'))


# Notice that we need to pass the `Duct` object, in this case `rect_duct`, to the constructor of the fitting. Fittings can be assigned an ID and may need additional parameters, such as the angle of the elbow in this example. 

# The loss or resistance coefficient of a fitting can be retrieved through its property `zeta`. The Greek letter *zeta* (ζ) is often used in literature to designate the loss coefficient of a fitting.

# In[34]:


ja.display_list([
    f"loss coefficient of elbow: <b>{elbow.zeta:.3f}</b>"
])


# **Add the Fitting to the Duct**

# To distinguish between the different fittings in a duct, a name or ID can be assigned to a fitting. To add the fitting to the duct, we need to pass its loss coefficient and ID to the duct.

# In[35]:


rect_duct.add_fitting(zeta=elbow.zeta, ID=elbow.ID)


# Adding fittings to a duct, will mostly increase the pressure drop across the duct caused by the air flow. After the fitting has been added to the duct, we can check its effect on the pressure drop:

# In[36]:


ja.display_list([
    f"total pressure drop along the duct: <b>{rect_duct.pressure_drop.to('Pa'):~P.3f}</b>"
])


# In[ ]:




