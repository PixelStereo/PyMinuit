#!/usr/bin/env python 

#################
# Minuit Module
# Pixel Stereo - 2014/2015
################################
import socket

#init empty listen dict
m_listen = {}


def oscquery (sender,query,node,args):
	#this is a 'namespace' query
	if query == 'namespace':
		address = 'modul8:namespace'
		if node == '/' :
			attributes = ['version' , 'name' , 'author']
			answer = ['/' , 'Application' , 'nodes={' , m_namespace['data'].keys() , '}' , 'attributes={' , attributes , '}']
			if print_minuit_output : print "MINUIT OUTPUT : ", address , answer
			modul8.sendOSC(address,answer)
		else:
			if len(node.split('/')) > 2:
				# need to know if it is a node or a leaf
				# a node has a data content, and a leaf hasn't
				m_node = node.split('/')[1:]
				if len(m_node) == 2:
					if 'data' in m_namespace['data'][m_node[0]]['data'][m_node[1]].keys():
						answer = [node , 'Container' , 'nodes={' , m_namespace['data'][m_node[0]]['data'][m_node[1]]['data'].keys() , '}' , 'attributes={' 'priority' , 'tags' , 'service' , '}']
					else:
						answer = [node , 'Data' , 'attributes ={' , m_namespace['data'][m_node[0]]['data'][m_node[1]]['attributes'].keys() , '}']
				elif len(m_node) == 3:
					if 'data' in m_namespace['data'][m_node[0]]['data'][m_node[1]]['data'][m_node[2]].keys():
						answer = [node , 'Container' , 'nodes={' , m_namespace['data'][m_node[0]]['data'][m_node[1]]['data'][m_node[2]]['data'].keys() , '}' , 'attributes={' 'priority' , 'tags' , 'service' , '}']
					else:
						answer = [node , 'Data' , 'attributes ={' , m_namespace['data'][m_node[0]]['data'][m_node[1]]['data'][m_node[2]]['attributes'].keys() , '}']
				elif len(m_node) == 4:
					if 'data' in m_namespace['data'][m_node[0]]['data'][m_node[1]]['data'][m_node[2]]['data'][m_node[3]].keys():
						answer = [node , 'Container' , 'nodes={' , m_namespace['data'][m_node[0]]['data'][m_node[1]]['data'][m_node[2]]['data'][m_node[3]]['data'].keys() , '}' , 'attributes={' 'priority' , 'tags' , 'service' , '}']
					else:
						answer = [node , 'Data' , 'attributes ={' , m_namespace['data'][m_node[0]]['data'][m_node[1]]['data'][m_node[2]]['data'][m_node[3]]['attributes'].keys() , '}']
				if print_minuit_output : print "MINUIT OUTPUT : ", address , answer
				modul8.sendOSC(address,answer)
			else:
				m_node = node.split('/')[1]
				answer = [node , 'Container' , 'nodes={' , m_namespace['data'][m_node]['data'].keys() , '}' , 'attributes={' 'priority' , 'tags' , 'service' , '}']
				if print_minuit_output : print "MINUIT OUTPUT : ", address , answer
				modul8.sendOSC(address,answer)
	#this is a 'get' query
	elif query == 'get':
		address = 'modul8:get'
		m_node = node.split(':')[:1][0]
		get_request = node.split(':')[1:][0]
		if m_node == '/':
			answer = [node , m_namespace['attributes'][get_request]]
		else:		
			m_node = m_node.split('/')
			m_node = m_node[1:]	
			if len(m_node) == 1:					
				answer = [node , m_namespace['data'][m_node[0]]['attributes'][get_request]]
			elif len(m_node) == 2:
				answer = [node , m_namespace['data'][m_node[0]]['data'][m_node[1]]['attributes'][get_request]]
			elif len(m_node) == 3:
				answer = [node , m_namespace['data'][m_node[0]]['data'][m_node[1]]['data'][m_node[2]]['attributes'][get_request]]
			elif len(m_node) == 4:
				answer = [node , m_namespace['data'][m_node[0]]['data'][m_node[1]]['data'][m_node[2]]['data'][m_node[3]]['attributes'][get_request]]
		#i-score doesn't support True or False, but 1 or 0
		if answer[1] == True : answer[1] = 1
		if answer[1] == False : answer[1] = 0
		if print_minuit_output : print "MINUIT OUTPUT : ", address , answer
		modul8.sendOSC(address,answer)
	#this is a 'listen' query
	elif query == 'listen':
		address = 'modul8:listen'
		keyword = node
		keyword = keyword.split('/')[1:]
		if keyword[0] == 'master':
			layer_index = 'master'
			keyword = 'ctrl_' + '_'.join(keyword)
		elif keyword[0] == 'mask':
			layer_index = 'mask'
			keyword =  '_'.join(keyword)
		else:
			layer_index = keyword[0]
			keyword = keyword[1:]
			keyword = 'ctrl_layer_' + '_'.join(keyword)
		args = args[0]
		data = keyword.split(':')[:1][0]
		# if request is '/' (root), clear the listen dict
		if keyword == 'ctrl_layer_' :
			pass
		else:
			attribut = keyword.split(':')[1]
			if args == 'enable':
				#add m_node to 'm_listen' dictionary
				m_listen.setdefault(layer_index,{})
				m_listen[layer_index].update({data:attribut})
			elif args == 'disable':
				del m_listen[layer_index][data]

# This function need to be call when there is something coming from the network (incoming OSC messages)
if type == 'OSC':
	#this is a Minuit query
	if '?' in param['address']:
		if print_minuit_input : print "MINUIT INPUT : ",  param['address'] , param['args']
		sender = param['address'].split('?')[0]
		query = param['address'].split('?')[1]
		node = param['args'][0]
		args = param['args'][1:]
		oscquery(sender,query,node,args)
	#this is a Minuit error
	elif '!' in param['address']:
		if print_minuit_input : print "MINUIT ERROR : ",  param['address'] , param['args']
		print 'error :' , 	param
	#this is a Minuit answer (it won't be used for the 0.2 version of this module)
	elif ':' in param['address']:
		if print_minuit_input : print "MINUIT INPUT : ",  param['address'] , param['args']
		print 'answer is not supported in this version of this module'
	#this is an OSC message
	elif '/' == param['address'][0]:
		if print_osc_input : print "OSC INPUT : ", param['address'] , param['args']
		keyword = param['address']
		keyword = keyword.split('/')[1:]
		if keyword[0] == 'master':
			layer_index = 0
			keyword = 'ctrl_' + '_'.join(keyword)
		elif keyword[0] == 'mask':
			layer_index = 0
			keyword = 'direct_globalMask_' + '_'.join(keyword[1:])
		else:
			layer_index = keyword[0].split('.')[1]
			# support wildcard for instances
			if layer_index == '*':
				layer_index = -1
			else:
				layer_index = int(layer_index)
			keyword = keyword[1:]
			keyword = 'ctrl_layer_' + '_'.join(keyword)
		modul8.setValue(keyword, param['args'][0], layer_index)

#This function need to be call when there is values changing in the python application
if layer > 0:
	layer_index = 'layer.' + str(layer)
if keyword.startswith ('ctrl_master') :	
	layer_index = 'master'
if keyword.startswith ('direct_globalMask') :	
	layer_index = 'mask'
	keyword = keyword = keyword.split('_')
	keyword = keyword[2:]
	bogus = ['mask']
	keyword = bogus + keyword 
	keyword = '_'.join(keyword)
if keyword == 'ctrl_layer_auto_scaleXY_':
	keyword = 'ctrl_layer_auto_scaleXY	'
if layer_index in m_listen.keys() :
	if keyword in m_listen[layer_index].keys() :
		if m_listen[layer_index][keyword] == 'value':
			keyword = keyword.split('_')
			if layer_index == 'mask' :
				keyword = keyword[1:]
			else : 
				keyword = keyword[2:]
			keyword = '/'.join(keyword)
			address = '/' + '/'.join([layer_index,keyword])
			#i-score doesn't support True or False, but 1 or 0
			if param == True : param = 1
			if param == False : param = 0
			if print_osc_output : print "OSC OUTPUT : ",  address, param
			modul8.sendOSC('modul8:listen' , address , param)