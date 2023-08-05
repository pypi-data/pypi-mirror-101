from localstack.utils.aws import aws_models
KjVGn=super
KjVGq=None
KjVGr=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KjVGn(LambdaLayer,self).__init__(arn)
  self.cwd=KjVGq
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.KjVGr.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,KjVGr,env=KjVGq):
  KjVGn(RDSDatabase,self).__init__(KjVGr,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,KjVGr,env=KjVGq):
  KjVGn(RDSCluster,self).__init__(KjVGr,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,KjVGr,env=KjVGq):
  KjVGn(AppSyncAPI,self).__init__(KjVGr,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,KjVGr,env=KjVGq):
  KjVGn(AmplifyApp,self).__init__(KjVGr,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,KjVGr,env=KjVGq):
  KjVGn(ElastiCacheCluster,self).__init__(KjVGr,env=env)
class TransferServer(BaseComponent):
 def __init__(self,KjVGr,env=KjVGq):
  KjVGn(TransferServer,self).__init__(KjVGr,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,KjVGr,env=KjVGq):
  KjVGn(CloudFrontDistribution,self).__init__(KjVGr,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,KjVGr,env=KjVGq):
  KjVGn(CodeCommitRepository,self).__init__(KjVGr,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
