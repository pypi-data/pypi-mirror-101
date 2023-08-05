from localstack.utils.aws import aws_models
jgJzM=super
jgJzX=None
jgJzI=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  jgJzM(LambdaLayer,self).__init__(arn)
  self.cwd=jgJzX
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.jgJzI.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,jgJzI,env=jgJzX):
  jgJzM(RDSDatabase,self).__init__(jgJzI,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,jgJzI,env=jgJzX):
  jgJzM(RDSCluster,self).__init__(jgJzI,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,jgJzI,env=jgJzX):
  jgJzM(AppSyncAPI,self).__init__(jgJzI,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,jgJzI,env=jgJzX):
  jgJzM(AmplifyApp,self).__init__(jgJzI,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,jgJzI,env=jgJzX):
  jgJzM(ElastiCacheCluster,self).__init__(jgJzI,env=env)
class TransferServer(BaseComponent):
 def __init__(self,jgJzI,env=jgJzX):
  jgJzM(TransferServer,self).__init__(jgJzI,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,jgJzI,env=jgJzX):
  jgJzM(CloudFrontDistribution,self).__init__(jgJzI,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,jgJzI,env=jgJzX):
  jgJzM(CodeCommitRepository,self).__init__(jgJzI,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
