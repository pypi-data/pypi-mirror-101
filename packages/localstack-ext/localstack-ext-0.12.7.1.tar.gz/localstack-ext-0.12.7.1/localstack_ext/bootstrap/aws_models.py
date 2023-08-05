from localstack.utils.aws import aws_models
esFSC=super
esFSX=None
esFSx=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  esFSC(LambdaLayer,self).__init__(arn)
  self.cwd=esFSX
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.esFSx.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,esFSx,env=esFSX):
  esFSC(RDSDatabase,self).__init__(esFSx,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,esFSx,env=esFSX):
  esFSC(RDSCluster,self).__init__(esFSx,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,esFSx,env=esFSX):
  esFSC(AppSyncAPI,self).__init__(esFSx,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,esFSx,env=esFSX):
  esFSC(AmplifyApp,self).__init__(esFSx,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,esFSx,env=esFSX):
  esFSC(ElastiCacheCluster,self).__init__(esFSx,env=env)
class TransferServer(BaseComponent):
 def __init__(self,esFSx,env=esFSX):
  esFSC(TransferServer,self).__init__(esFSx,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,esFSx,env=esFSX):
  esFSC(CloudFrontDistribution,self).__init__(esFSx,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,esFSx,env=esFSX):
  esFSC(CodeCommitRepository,self).__init__(esFSx,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
