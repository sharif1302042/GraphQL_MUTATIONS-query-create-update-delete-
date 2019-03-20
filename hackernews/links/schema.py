import graphene

from graphene_django import DjangoObjectType
from .models import Link

class LinkType(DjangoObjectType):
    class Meta:
        model = Link
"""
###################################################################
                               QUERY
###################################################################
"""
class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

"""
###################################################################
                           Create
###################################################################
"""

class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        link=Link(url=url, description=description)
        link.save()
        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )

"""
###################################################################
                              Delete
###################################################################
"""

class DeleteLink(graphene.Mutation):
    id= graphene.Int()

    class Arguments:
        id = graphene.Int()
        description = graphene.String()

    def mutate(self,info, id):
        instance=Link.objects.get(id=id)
        if instance:
            instance.delete()
            return DeleteLink(
                id=id
            )
        return None

"""
###################################################################
                          Update
###################################################################
"""
class LinkInput(graphene.InputObjectType):
    id = graphene.ID()
    url = graphene.String()
    description = graphene.String()

class UpdateLink(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id =graphene.Int()
        url = graphene.String()
        description = graphene.String()

    def mutate(self,info,id,url,description):
        instance=Link.objects.get(id=id)
        if instance:
            instance.description = description
            instance.url=url
            instance.save()
            return UpdateLink(id=id)
        return None


class Mutation(graphene.ObjectType):
    create_link= CreateLink.Field()
    delete_link = DeleteLink.Field()
    update_link = UpdateLink.Field()




"""
###################################################################
                          Delete
###################################################################

mutation{
  deleteLink(id: 6){
    id
  }
}


###################################################################
                          Update
###################################################################

mutation{
  updateLink(id:2,url:"home.com",description:"this is home page"){
    id

  }
}


########################################################
                       Token Auth
########################################################

mutation{
  tokenAuth(username: "s",password:"s1234567"){
    token
    
  }
}
########################################################
                        Varify Token
#####################################################
mutation{
  verifyToken( token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InMiLCJleHAiOjE1NTMwNzUyMTYsIm9yaWdfaWF0IjoxNTUzMDc0OTE2fQ.igV7f1AUM7E5XNPfyQQFr8AeGYmi0cPaXBKiucvnaeY")
  {
    payload
    
  }
}
########################################################
                        users creation
#####################################################
"""


