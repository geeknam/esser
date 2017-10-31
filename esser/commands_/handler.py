from esser.repositories.dynamodb import DynamoDBRepository


class BaseCommandHandler(object):

    repository = DynamoDBRepository

    def __init__(self):
        pass

    