from localstack.utils.aws import aws_models
gPoCh=super
gPoCM=None
gPoCi=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  gPoCh(LambdaLayer,self).__init__(arn)
  self.cwd=gPoCM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.gPoCi.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,gPoCi,env=gPoCM):
  gPoCh(RDSDatabase,self).__init__(gPoCi,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,gPoCi,env=gPoCM):
  gPoCh(RDSCluster,self).__init__(gPoCi,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,gPoCi,env=gPoCM):
  gPoCh(AppSyncAPI,self).__init__(gPoCi,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,gPoCi,env=gPoCM):
  gPoCh(AmplifyApp,self).__init__(gPoCi,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,gPoCi,env=gPoCM):
  gPoCh(ElastiCacheCluster,self).__init__(gPoCi,env=env)
class TransferServer(BaseComponent):
 def __init__(self,gPoCi,env=gPoCM):
  gPoCh(TransferServer,self).__init__(gPoCi,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,gPoCi,env=gPoCM):
  gPoCh(CloudFrontDistribution,self).__init__(gPoCi,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,gPoCi,env=gPoCM):
  gPoCh(CodeCommitRepository,self).__init__(gPoCi,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
