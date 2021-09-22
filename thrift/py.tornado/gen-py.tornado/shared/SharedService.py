#
# Autogenerated by Thrift Compiler (0.15.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:tornado
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from tornado import gen
from tornado import concurrent
all_structs = []


class Iface(object):
    def getStruct(self, key):
        """
        Parameters:
         - key

        """
        pass


class Client(Iface):
    def __init__(self, transport, iprot_factory, oprot_factory=None):
        self._transport = transport
        self._iprot_factory = iprot_factory
        self._oprot_factory = (oprot_factory if oprot_factory is not None
                               else iprot_factory)
        self._seqid = 0
        self._reqs = {}
        self._transport.io_loop.spawn_callback(self._start_receiving)

    @gen.engine
    def _start_receiving(self):
        while True:
            try:
                frame = yield self._transport.readFrame()
            except TTransport.TTransportException as e:
                for future in self._reqs.values():
                    future.set_exception(e)
                self._reqs = {}
                return
            tr = TTransport.TMemoryBuffer(frame)
            iprot = self._iprot_factory.getProtocol(tr)
            (fname, mtype, rseqid) = iprot.readMessageBegin()
            method = getattr(self, 'recv_' + fname)
            future = self._reqs.pop(rseqid, None)
            if not future:
                # future has already been discarded
                continue
            try:
                result = method(iprot, mtype, rseqid)
            except Exception as e:
                future.set_exception(e)
            else:
                future.set_result(result)

    def getStruct(self, key):
        """
        Parameters:
         - key

        """
        self._seqid += 1
        future = self._reqs[self._seqid] = concurrent.Future()
        self.send_getStruct(key)
        return future

    def send_getStruct(self, key):
        oprot = self._oprot_factory.getProtocol(self._transport)
        oprot.writeMessageBegin('getStruct', TMessageType.CALL, self._seqid)
        args = getStruct_args()
        args.key = key
        args.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def recv_getStruct(self, iprot, mtype, rseqid):
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = getStruct_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationException.MISSING_RESULT, "getStruct failed: unknown result")


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["getStruct"] = Processor.process_getStruct
        self._on_message_begin = None

    def on_message_begin(self, func):
        self._on_message_begin = func

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if self._on_message_begin:
            self._on_message_begin(name, type, seqid)
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            return self._processMap[name](self, seqid, iprot, oprot)

    @gen.coroutine
    def process_getStruct(self, seqid, iprot, oprot):
        args = getStruct_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = getStruct_result()
        msg_type = TMessageType.REPLY
        try:
            result.success = yield gen.maybe_future(self._handler.getStruct(args.key))
        except TTransport.TTransportException:
            raise
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("getStruct", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

# HELPER FUNCTIONS AND STRUCTURES


class getStruct_args(object):
    """
    Attributes:
     - key

    """


    def __init__(self, key=None,):
        self.key = key

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.key = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('getStruct_args')
        if self.key is not None:
            oprot.writeFieldBegin('key', TType.I32, 1)
            oprot.writeI32(self.key)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(getStruct_args)
getStruct_args.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'key', None, None, ),  # 1
)


class getStruct_result(object):
    """
    Attributes:
     - success

    """


    def __init__(self, success=None,):
        self.success = success

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = SharedStruct()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('getStruct_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(getStruct_result)
getStruct_result.thrift_spec = (
    (0, TType.STRUCT, 'success', [SharedStruct, None], None, ),  # 0
)
fix_spec(all_structs)
del all_structs
