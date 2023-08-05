from localstack.utils.aws import aws_models
PWVna=super
PWVnN=None
PWVnA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  PWVna(LambdaLayer,self).__init__(arn)
  self.cwd=PWVnN
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.PWVnA.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,PWVnA,env=PWVnN):
  PWVna(RDSDatabase,self).__init__(PWVnA,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,PWVnA,env=PWVnN):
  PWVna(RDSCluster,self).__init__(PWVnA,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,PWVnA,env=PWVnN):
  PWVna(AppSyncAPI,self).__init__(PWVnA,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,PWVnA,env=PWVnN):
  PWVna(AmplifyApp,self).__init__(PWVnA,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,PWVnA,env=PWVnN):
  PWVna(ElastiCacheCluster,self).__init__(PWVnA,env=env)
class TransferServer(BaseComponent):
 def __init__(self,PWVnA,env=PWVnN):
  PWVna(TransferServer,self).__init__(PWVnA,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,PWVnA,env=PWVnN):
  PWVna(CloudFrontDistribution,self).__init__(PWVnA,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,PWVnA,env=PWVnN):
  PWVna(CodeCommitRepository,self).__init__(PWVnA,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
