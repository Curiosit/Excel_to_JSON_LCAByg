#!/usr/bin/env python
# coding: utf-8
# Mateusz Płoszaj-Mazurek
# Sources
# https://www.lcabyg.dk/en/bim-integration-eng-2/
# https://thinkmoult.com/using-ifcopenshell-parse-ifc-files-python.html
# https://github.com/johannesmichael/ifc-python/blob/master/modules/ifc_pset_utils.py
# https://www.kaggle.com/code/ponybiam/introduction-to-ifcopenshell-functions/notebook
# https://blenderbim.org/docs-python/ifcopenshell-python/hello_world.html


import json
import ifcHelper
import pandas as pd
import numpy as np
import uuid


comment = "Created by Excel_to_JSON_LCAByg. https://github.com/Curiosit/Excel_to_JSON_LCAByg"

def add_things_json_list(json_list, json_element):
    for i in json_element:
        json_list.append(i)
    return json_list

def create_lcabyg_elements():
    
    json_array_elements = []
    json_array_constructions = []
    json_array_element_category = []
    json_array_constructions_extra = []
    
    lcabyg_elements = json_array_elements, json_array_constructions,json_array_element_category, json_array_constructions_extra
    
    return lcabyg_elements

def append_lcabyg_element(lcabyg_elements, construction_amount, construction_name = 'Test_construction', element_name = 'Test_element', unit = 'M2', layers='', products_df='', element_id = str(uuid.uuid4()), lifespan = 50, product_id = '51bcec85-9105-4946-8a8a-51219bf9adfa'):
    
    ################ SET PROPERTIES AND IDs
    
    #element_id = str(uuid.uuid4())
    #construction_id = str(uuid.uuid4())
    element_category_id = str(uuid.uuid4())
    
    construction_edge_id = str(uuid.uuid4())
    
    element_category_edge_id = str(uuid.uuid4())
    constructions_category_id = str(uuid.uuid4())
    
    ################ DEFAULT IDs (this ones are not needed to change)
    
   
    
    ################ DEFAULT IDs from example
    #element_id = '02c3e303-a443-4f02-9927-e43519227ade'
    #construction_id = 'c6f24e0f-020a-4f0f-93c6-65beb50bd798'
    element_category_id = '069983d0-d08b-405b-b816-d28ca9648956'
    product_id_m2 ='51bcec85-9105-4946-8a8a-51219bf9adfa' #m2
    product_id_m = '5dcafff0-1ec7-49e7-b425-fff6d1a0e03f' #m
    
    
    #construction_edge_id = '65cc0492-7864-4598-9254-5f929379bae6'
    #element_edge_id = 'e66c3d76-eae6-4c6b-86f7-e9178bc8f804'
    #element_category_edge_id = '479c5e5a-b173-4c07-bfbd-0cedff55888b'
    constructions_category_id = '8cef6e2a-ad53-4450-9c6f-7a24eb9fcf16'
    
    
    ################
    ## LOAD JSON ARRAYS
    
    json_array_elements = lcabyg_elements[0]
    json_array_constructions = lcabyg_elements[1]
    json_array_element_category = lcabyg_elements[2]
    json_array_constructions_extra = lcabyg_elements[3]
    
    
    ################ ELEMENTS.JSON
    element_properties = {'id': element_id,  "name": { "Danish": element_name,"English": "","German": "" }, "source": "User", "comment": comment, "enabled": True, "active": True}
    element_set = {'Element': element_properties}
    element_node = {'Node': element_set}
    
    
    element_edge_id = []
    construction_id = []
    construction_edge_id = []
    element_edges = []
    i = 0
    
    ####
    json_array_elements.append(element_node) #0 elements.json
    print ('Added element:')
    print (element_name)
    ####
    #print (construction_amount)
    for n in construction_amount:
        #print (n)
        print ('Added construction')
        print (construction_name[i])
        print (n)
        element_edge_id.append(str(uuid.uuid4()))
        construction_id.append(str(uuid.uuid4()))
        
        element_edge_details = {'id': element_edge_id[i],'amount': n, 'enabled': True}
        element_edge_data = [{'ElementToConstruction': element_edge_details}, element_id, construction_id[i]]
        element_edge = {'Edge': element_edge_data}
                 
        json_array_elements.append(element_edge) 
        
        
        ################ CONSTRUCTIONS.JSON
        product_id=''
        #print(unit[i])
        #if unit[i] == 'M2':
        #    product_id = product_id_m2
        #else:
        #    product_id = product_id_m
        
        construction_properties = {'id': construction_id[i],  'name': {'Danish': construction_name[i], 'English': 'Test construction'},'unit': unit[i], 'source': 'User','comment': comment,'layer': 1,'locked': True}
        construction_set = {'Construction': construction_properties}
        construction_node = {'Node': construction_set}
        
        json_array_constructions.append(construction_node) #1 constructions.json
        
        
        #product_id =  productid_df[i] 
        #product_ids = product_id.split('#')
        #print(product_ids)
        
        

        
        layers_split = layers[i].split('_')
        print('Layers:')
        print(layers_split)
        
        
        nn = 0
        previous_layer=''
        
        for layer in layers_split:
            print(layer)
            print('Products:')
            products = layer.rsplit(' ', 1)
            print(products[0])
            
            
            print('Amount from layer:')
            print(products[1])
            
            row = products_df[products_df['RevitNames'].str.contains(products[0])]
            row['Unit']
            if row['Unit'].values[0] == 'M3':
                print('M3')
                thickness = (float(products[1].replace(',', '.'))/100)*row['Amount'].values[0]
            else:
                if row['Unit'].values[0] == 'KG':
                    print('KG')
                    thickness = (float(products[1].replace(',', '.'))/100)*row['Amount'].values[0]
                else:
                    if row['Unit'].values[0] == 'M2':
                        thickness = row['Amount'].values[0]
                        print('_________')
                        print(row['Amount'].values[0])
                        print('M2')
                    else:
                        thickness = (float(products[1].replace(',', '.')))*row['Amount'].values[0]
                        print('Other unit')
                
                
            
            print('Previous layer:')
            print (previous_layer)
            if previous_layer=='Żelbet' and products[0]=='ZbrojZBbyratio':
                print('Reinforcement by ratio:')
                print(previous_amount)
                print(thickness)
                thickness = (thickness * previous_amount)/100
                print('Reinforcement amount:')
                print(thickness)
                
            
            print('Productid:')
            
            print(row['Productid'].values[0])
            print('LCABYG Name:')
            print(row['Row Labels'].values[0])
            
            productunit = row['Unit'].values[0]
            print('Final amount:')
            print(thickness)
            
            
            
            
            construction_edge_id = str(uuid.uuid4())
            construction_edge_details = {'id': construction_edge_id,'amount': float(thickness), 'unit': productunit, 'lifespan': lifespan,     'demolition': False,     'enabled': True,     'delayed_start': 0}
            construction_edge_data = [{'ConstructionToProduct': construction_edge_details}, construction_id[i], row['Productid'].values[0]]
            construction_edge = {'Edge': construction_edge_data}

            json_array_constructions.append(construction_edge)
            
            
            
            if products[0] == 'Żelbet':
                previous_layer='Żelbet'
                previous_amount=float(products[1])
            else:
                previous_layer=''
                previous_amount=0
            nn += 1
        

        
        ################ constructions_extra.json

        constructions_category_edge_details = {'id': str(uuid.uuid4()),'layers': [1]}
        constructions_category_edge_data = [{'CategoryToConstruction':constructions_category_edge_details}, element_category_id, construction_id[i]]
        constructions_category_edge = {'Edge': constructions_category_edge_data}

        ################ SAVE TO ARRAY

        
        json_array_constructions_extra.append(constructions_category_edge) #3 constructions_extra.json
        
        
        
        ########
        i += 1
    ############
    
    
    ################ element_category_edges.json
        
    element_category_edge_details = {'id': str(uuid.uuid4()), 'enabled': True}
    element_category_edge_data = [{'CategoryToElement':element_category_edge_details}, element_category_id, element_id]
    element_category_edge = {'Edge': element_category_edge_data}
    json_array_element_category.append(element_category_edge) #2 construction_category_edges.json
    
    
    

                            
    return  json_array_elements, json_array_constructions,json_array_element_category, json_array_constructions_extra



###########


def get_wall_dataframe(ifc_file):
    walls = ifc_file.by_type('IfcWall')
    walls_volumes = list()
    walls_thickness = list()
    walls_areas = list()
    walls_types = list()
    for i in range(len(walls)):
        quantities = ifcHelper.get_quantity_single_value(ifcHelper.get_related_quantities(walls[i])[0])
        walls_volumes.append(quantities['NetVolume'])
        walls_thickness.append(quantities['Width']/1000)
        walls_areas.append(walls_volumes[i]/walls_thickness[i])
        walls_types.append(walls[i].ObjectType)
        
    d = {'Type':walls_types,'Area':walls_areas}
    wall_df = pd.DataFrame(d)
    wall_types_sum = wall_df.groupby('Type')['Area'].sum().reset_index()
    
    try:
      wall_types_sum_df = pd.DataFrame(wall_types_sum)
      print("Walls loaded successfully")
    except:
      print("An exception occurred")
    return wall_types_sum_df


def get_slabs_dataframe(ifc_file):
    slabs = ifc_file.by_type('IfcSlab')
    slabs_areas = list()
    slabs_types = list()
    for i in range(len(slabs)):
        quantities_slabs = ifcHelper.get_quantity_single_value(ifcHelper.get_related_quantities(slabs[i])[0])
        slabs_areas.append(quantities_slabs['NetArea'])
        slabs_types.append(slabs[i].ObjectType)
        
    d_s = {'Type':slabs_types,'Area':slabs_areas}
    slabs_df = pd.DataFrame(d_s)
    slabs_types_sum = slabs_df.groupby('Type')['Area'].sum().reset_index()

    try:
      slabs_types_sum_df = pd.DataFrame(slabs_types_sum)
      print("Slabs loaded successfully")
    except:
      print("An exception occurred")
    return slabs_types_sum_df

def get_windows_dataframe(ifc_file):
    windows = ifc_file.by_type('IfcWindow')
    windows_types = list()
    windows_areas = list()
    for i in range(len(windows)):
        quantities_windows = ifcHelper.get_quantity_single_value(ifcHelper.get_related_quantities(windows[i])[0])
        windows_areas.append(quantities_windows['Area'])
        windows_types.append(windows[i].ObjectType)

    w_s = {'Type':windows_types,'Area':windows_areas}
    windows_df = pd.DataFrame(w_s)
    windows_types_sum = windows_df.groupby('Type')['Area'].sum().reset_index()

    try:
      windows_types_sum_df = pd.DataFrame(windows_types_sum)
      print("Windows loaded successfully")
    except:
      print("An exception occurred")
    return windows_types_sum_df


def get_doors_dataframe(ifc_file):
    doors = ifc_file.by_type('IfcDoor')
    doors_types = list()
    doors_areas = list()
    for i in range(len(doors)):
        quantities_doors = ifcHelper.get_quantity_single_value(ifcHelper.get_related_quantities(doors[i])[0])
        doors_areas.append(quantities_doors['Area'])
        doors_types.append(doors[i].ObjectType)

    dr_s = {'Type':doors_types,'Area':doors_areas}
    doors_df = pd.DataFrame(dr_s)
    doors_types_sum = doors_df.groupby('Type')['Area'].sum().reset_index()

    try:
      doors_types_sum_df = pd.DataFrame(doors_types_sum)
      print("Doors loaded successfully")
    except:
      print("An exception occurred")
    return doors_types_sum_df


def get_railings_dataframe(ifc_file):
    railings = ifc_file.by_type('IfcRailing')
    railings_types = list()
    railings_lengths = list()
    for i in range(len(railings)):
        quantities_railings = ifcHelper.get_quantity_single_value(ifcHelper.get_related_quantities(railings[i])[0])
        railings_lengths.append(quantities_railings['Length'])
        railings_types.append(railings[i].ObjectType)

    rl_s = {'Type':railings_types,'Length':railings_lengths}
    railings_df = pd.DataFrame(rl_s)
    railings_types_sum = railings_df.groupby('Type')['Length'].sum().reset_index()

    try:
      railings_types_sum_df = pd.DataFrame(railings_types_sum)
      print("Railings loaded successfully")
    except:
      print("An exception occurred")
    return railings_types_sum_df
def get_cw_panels_dataframe(ifc_file):
    cw_panels = ifc_file.by_type('IfcPlate')
    cw_panels_types = list()
    cw_panels_areas = list()
    for i in range(len(cw_panels)):
        cw_panels_areas.append(ifcHelper.get_property_single_value(ifcHelper.get_related_property_sets(cw_panels[i])[1])['Area'])
        cw_panels_types.append(cw_panels[i].ObjectType)


    cw_p_s = {'Type':cw_panels_types,'Area':cw_panels_areas}
    cw_panels_df = pd.DataFrame(cw_p_s)
    cw_panels_types_sum = cw_panels_df.groupby('Type')['Area'].sum().reset_index()

    try:
      cw_panels_types_sum_df = pd.DataFrame(cw_panels_types_sum)
      print("Curtain Wall panels loaded successfully")
    except:
      print("An exception occurred")
    return cw_panels_types_sum_df

def get_cw_mullions_dataframe(ifc_file):
    cw_mullions = ifc_file.by_type('IfcMember')
    cw_mullions_types = list()
    cw_mullions_lengths = list()
    for i in range(len(cw_mullions)):
        quantities_cw_mullions = ifcHelper.get_quantity_single_value(ifcHelper.get_related_quantities(cw_mullions[i])[0])
        cw_mullions_lengths.append(quantities_cw_mullions['Length']/1000)
        cw_mullions_types.append(cw_mullions[i].ObjectType)


    cw_m_s = {'Type':cw_mullions_types,'Length':cw_mullions_lengths}
    cw_mullions_df = pd.DataFrame(cw_m_s)
    cw_mullions_types_sum = cw_mullions_df.groupby('Type')['Length'].sum().reset_index()

    try:
      cw_mullions_types_sum_df =  pd.DataFrame(cw_mullions_types_sum)
      print("Curtain Wall panels loaded successfully")
    except:
      print("An exception occurred")
    return cw_mullions_types_sum_df 
