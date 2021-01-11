from src.typeDefs.element import IElement


class ITransformer(IElement):
    mvaCapacity: str
    transformerType: str
