# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import re
import etconfig

MY_CONF=u"""
        # this is a comment
        network {
            name="mynet1nâme"
            forward.mode=nat
            forward.nat.port {start=1024 end=65535}
            ip {
               address=10.20.30.1
               netmask=255.255.255.0
               dhcp.range {start=10.20.30.40 end=10.20.30.254}
            }
        }
"""

def test_loads():
        config = etconfig.loads(MY_CONF)
        assert config is not None
        assert config.find("network/ip").get("address") == "10.20.30.1"
        assert config.find("network").get("name") == "mynet1nâme"


def test_dumps():
        config = etconfig.loads(MY_CONF)
        dump = etconfig.dumps(config)
        dump_no_spaces = re.sub(r'\s', '', dump)
        expected = u'root{network{name="mynet1nâme"forward{mode=natnat{port{start=1024end=65535}}}ip{address=10.20.30.1netmask=255.255.255.0dhcp{range{start=10.20.30.40end=10.20.30.254}}}}}'

        print(dump.encode("utf8"))
        print(dump_no_spaces.encode("utf8"))
        assert dump_no_spaces==expected


def test_single_root():
        CNF = u"""
# a comment
node2 {
        // comment
        a=2
        node11 {
            b=8;c=13;
        }

}
"""
        config = etconfig.loads(CNF, single_root_node=True)
        dump=etconfig.dumps(config)
        dump_no_spaces = re.sub(r'\s', '', dump)
        print(dump.encode('utf8'))
        assert(config.tag=="node2")
        assert(config.get("a") =="2")
        assert(config.find("node11").get("b") =="8")
        assert(dump_no_spaces=='node2{a=2node11{b=8c=13}}')

def test_id2attr():
        CNF = u"""
# a comment
node2 abcd {
        // comment
        a=2
        node11 {
            b=8;c=13;
        }

}
"""
        config = etconfig.loads(CNF, single_root_node=True,
                                id_mapper=etconfig.id2attr('foo'))
        dump=etconfig.dumps(config)
        dump_no_spaces = re.sub(r'\s', '', dump)
        print(dump.encode('utf8'))
        assert(config.tag=="node2")
        assert(config.get("a") =="2")
        assert(config.get("foo") =="abcd")
        assert(config.find("node11").get("b") =="8")
        assert(dump_no_spaces=='node2{a=2foo=abcdnode11{b=8c=13}}')

def test_id2elt():
        CNF = u"""node2 abcd { a = 2 node11 { b = 8 c = 13 } }"""
        config = etconfig.loads(CNF, single_root_node=True,
                                id_mapper=etconfig.id2elt('bar'))
        dump=etconfig.dumps(config)
        dump_no_spaces = re.sub(r'\s+', ' ', dump)
        print(dump.encode('utf8'))
        assert(config.tag=="node2")
        assert(config.get("a") =="2")
        assert(config.find("bar").text =="abcd")
        assert(config.find("node11").get("b") =="8")
        assert(dump_no_spaces=='node2 { a = 2 bar abcd; node11 { b = 8 c = 13 } } ')


def test_text():
        CNF = u"""

node1 "this is têxt";

node2 {
        // comment
        node11 "this îs also text";
}

node3 {"still\na\ttèxt"}
node4 {
        "yet änother"
        more=stuff
}


"""
        config = etconfig.loads(CNF, root_name='bla')
        dump=etconfig.dumps(config)
        dump_no_spaces = re.sub(r'\s', '', dump)
        print(dump.encode('utf8'))
        assert(config.tag=="bla")
        assert(config.find("node1").text=="this is têxt")
        assert(config.find("node2/node11").text=="this îs also text")
        assert(config.find("node3").text=="still\na\ttèxt")
        assert(config.find("node4").text=="yet änother")
        assert(dump_no_spaces=='bla{node1"thisistêxt";node2{node11"thisîsalsotext";}node3"stillatèxt";node4{"yetänother"more=stuff}}')


def test_custom_root_name():
        CNF = u"""node2 {x=3}"""
        config = etconfig.loads(CNF, root_name='bla')
        dump=etconfig.dumps(config)
        dump_no_spaces = re.sub(r'\s', '', dump)
        print(dump.encode('utf8'))
        assert(config.tag=="bla")
        assert(config.find("node2").get("x")=="3")
        assert(dump_no_spaces=='bla{node2{x=3}}')


# todo test not passing. parsing error
def __test_multiline_string():
        CNF = u"""
/* this is à multiline
   comment
*/

// this is a c-style cômment

multiline1=```begin
lîne1
lïne2
end```

node1 {
    subnode11 ```begin
lîne1
lïne2
end```;


}

"""
        config = etconfig.loads(CNF)
        print(etconfig.dumps(config).encode('utf8'))

        assert config is not None
        assert config.get("multiline1") == u"begin\nlîne1\nlïne2\nend"
        assert config.find("node1").get("multiline2") == u"bégin\nlîne1\nlïne2\nend"
        # assert config==""

