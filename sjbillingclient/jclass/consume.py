from jnius import JavaClass, MetaJavaClass, JavaStaticMethod

__all__ = ("ConsumeParams",)


class ConsumeParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/ConsumeParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/ConsumeParams$Builder;")
