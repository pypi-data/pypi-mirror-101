from localstack.utils.aws import aws_models
fOseV=super
fOsez=None
fOsek=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  fOseV(LambdaLayer,self).__init__(arn)
  self.cwd=fOsez
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.fOsek.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,fOsek,env=fOsez):
  fOseV(RDSDatabase,self).__init__(fOsek,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,fOsek,env=fOsez):
  fOseV(RDSCluster,self).__init__(fOsek,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,fOsek,env=fOsez):
  fOseV(AppSyncAPI,self).__init__(fOsek,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,fOsek,env=fOsez):
  fOseV(AmplifyApp,self).__init__(fOsek,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,fOsek,env=fOsez):
  fOseV(ElastiCacheCluster,self).__init__(fOsek,env=env)
class TransferServer(BaseComponent):
 def __init__(self,fOsek,env=fOsez):
  fOseV(TransferServer,self).__init__(fOsek,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,fOsek,env=fOsez):
  fOseV(CloudFrontDistribution,self).__init__(fOsek,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,fOsek,env=fOsez):
  fOseV(CodeCommitRepository,self).__init__(fOsek,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
