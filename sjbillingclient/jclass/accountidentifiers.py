from jnius import JavaClass, MetaJavaClass, JavaMethod

__all__ = ("AccountIdentifiers",)


class AccountIdentifiers(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/AccountIdentifiers"

    getObfuscatedAccountId = JavaMethod("()Ljava/lang/String;")
    getObfuscatedProfileId = JavaMethod("()Ljava/lang/String;")
