import numpy as np
import re
import subprocess
from itertools import chain

import onnx
import onnxruntime as ort

import numpy as np

def predict_with_onnxruntime(model_def, *inputs):
    'run an onnx model'
    
    sess = ort.InferenceSession(model_def.SerializeToString())
    names = [i.name for i in sess.get_inputs()]

    inp = dict(zip(names, inputs))
    res = sess.run(None, inp)

    #names = [o.name for o in sess.get_outputs()]

    return res[0]

def remove_unused_initializers(model):
    'return a modified model'

    new_init = []

    for init in model.graph.initializer:
        found = False
        
        for node in model.graph.node:
            for i in node.input:
                if init.name == i:
                    found = True
                    break

            if found:
                break

        if found:
            new_init.append(init)
        else:
            print(f"removing unused initializer {init.name}")

    graph = onnx.helper.make_graph(model.graph.node, model.graph.name, model.graph.input,
                                   model.graph.output, new_init)

    onnx_model = make_model_with_graph(model, graph)

    return onnx_model

def make_model_with_graph(model, graph, ir_version=None, check_model=True):
    'copy a model with a new graph'

    onnx_model = onnx.helper.make_model(graph)
    onnx_model.ir_version = ir_version if ir_version is not None else model.ir_version
    onnx_model.producer_name = model.producer_name
    onnx_model.producer_version = model.producer_version
    onnx_model.domain = model.domain
    onnx_model.model_version = model.model_version
    onnx_model.doc_string = model.doc_string

    #print(f"making model with ir version: {model.ir_version}")
    
    if len(model.metadata_props) > 0:
        values = {p.key: p.value for p in model.metadata_props}
        onnx.helper.set_model_props(onnx_model, values)

    # fix opset import
    for oimp in model.opset_import:
        op_set = onnx_model.opset_import.add()
        op_set.domain = oimp.domain
        op_set.version = oimp.version

    if check_model:
        onnx.checker.check_model(onnx_model, full_check=True)

    return onnx_model

def glue_models(model1, model2):
    'glue the two onnx models into one'

    g1_in, g1_out = get_io_nodes(model1)
    g2_in, _ = get_io_nodes(model2)
    
    assert g1_out.name == g2_in.name, f"model1 output was {g1_out.name}, " + \
        f"but model2 input was {g2_in.name}"

    graph1 = model1.graph
    graph2 = model2.graph

    var_in = [g1_in]

    # sometimes initializers are added as inputs
    #for inp in graph2.input[1:]:
    #    var_in.append(inp)
    
    var_out = graph2.output

    combined_init = []
    names = []
    for init in chain(graph1.initializer, graph2.initializer):
        assert init.name not in names, f"repeated initializer name: {init.name}"
        names.append(init.name)

        combined_init.append(init)

    #print(f"initialier names: {names}")

    combined_nodes = []
    #names = []
    for n in chain(graph1.node, graph2.node):
        #assert n.name not in names, f"repeated node name: {n.name}"
        #names.append(n.name)

        combined_nodes.append(n)

    name = graph2.name
    graph = onnx.helper.make_graph(combined_nodes, name, var_in,
                       var_out, combined_init)

    #print(f"making model with inputs {inputs} / outputs {outputs} and nodes len: {len(keep_nodes)}")

    # use ir_version 4 because we don't add inputs as initializers
    onnx_model = make_model_with_graph(model2, graph, ir_version=4)

    return onnx_model

def findObjectiveFuncionType(spec):
   N=dict.fromkeys(range(5),0)
   M=dict.fromkeys(range(5),0)
   for j in range(len(spec)):
       arr=spec[j][0]
       print(arr)
       for k in range(len(arr)):
           for kk in range(len(arr[k])):
              if (arr[k][kk] != 0):
                 a=N.get(kk)+1
                 N[kk]=a
              if (arr[k][kk] < 0):
                 a=M.get(kk)+1
                 M[kk]=a

   target=max(N, key=N.get)
   objType=max(N, key=M.get)
   output=[]
   output.append(target)
   if (target == objType) :
      output.append(0) #Maximization
      print("Target:",target,"Objective :Max",)
   else:
      output.append(1) #Minimization
      print("Target:",target,"Objective :Min",)
   return output

def checkAndSegregateSamplesForMaximum(posSample,negSample, smple,oldPos,targetNode):      
    a=smple[0][1]
    large = a[targetNode]
    last_index=0
    posSample.append(smple[0])
    for i in range(1,len(smple)):
        a=smple[i][1]
        newLarge = a[targetNode]
        if newLarge > large :
            posSample.remove(smple[last_index])
            posSample.append(smple[i])
            negSample.append(smple[last_index])
            last_index=i
            large=newLarge
        else:
            if newLarge < large :
               negSample.append(smple[i])
    if (len(oldPos) > 0) :
        cPos=posSample[0][1]
        oldPos1=oldPos[0][1]
        if ( oldPos1[targetNode] > cPos[targetNode] ) :
            negSample.append(posSample[0])
            posSample.remove(posSample[0])
            posSample.append(oldPos[0])

def checkAndSegregateSamplesForMinimum(posSample,negSample, smple,oldPos,targetNode):      
    a=smple[0][1]
    small = a[targetNode]
    last_index=0
    posSample.append(smple[0])
    for i in range(1,len(smple)):
        a=smple[i][1]
        newSmall = a[targetNode]
        if newSmall < small :
            posSample.remove(smple[last_index])
            posSample.append(smple[i])
            negSample.append(smple[last_index])
            last_index=i
            small=newSmall
        else:
            if newSmall < small :
               negSample.append(smple[i])
    if (len(oldPos) > 0) :
        cPos=posSample[0][1]
        oldPos1=oldPos[0][1]
        if ( oldPos1[targetNode] < cPos[targetNode] ) :
            negSample.append(posSample[0])
            posSample.remove(posSample[0])
            posSample.append(oldPos[0])



