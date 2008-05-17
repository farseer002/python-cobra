#coding=utf-8
code2description = {
'LOAD_CONST' : '1、从consts列表中读取对象obj<br/>2、将obj压入运行时栈',
'STORE_NAME' : '1、从运行时栈中弹出对象obj<br/>2、将obj放入local名字空间中',
'LOAD_NAME' : '1、从local名字空间中搜索对象obj<br/>2、将obj压入运行时栈',
'BINARY_ADD' : '1、读取栈顶元素TOS(top of stack)<br/>2、读取栈顶次元素TOS1<br/>3、执行加法操作，重置栈顶元素，即：TOS = TOS1 + TOS',
'BUILD_MAP' : '1、创建一个空的dict对象obj<br/>2、将obj压入运行时栈',
'BUILD_LIST' : '参数：count<br/>1、创建包含count个元素的list对象obj，元素来自运行时栈<br/>2、将obj压入运行时栈',
}
