// Generated by gencpp from file audio_common_msgs/AudioData.msg
// DO NOT EDIT!


#ifndef AUDIO_COMMON_MSGS_MESSAGE_AUDIODATA_H
#define AUDIO_COMMON_MSGS_MESSAGE_AUDIODATA_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace audio_common_msgs
{
template <class ContainerAllocator>
struct AudioData_
{
  typedef AudioData_<ContainerAllocator> Type;

  AudioData_()
    : data()  {
    }
  AudioData_(const ContainerAllocator& _alloc)
    : data(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector<uint8_t, typename ContainerAllocator::template rebind<uint8_t>::other >  _data_type;
  _data_type data;





  typedef boost::shared_ptr< ::audio_common_msgs::AudioData_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::audio_common_msgs::AudioData_<ContainerAllocator> const> ConstPtr;

}; // struct AudioData_

typedef ::audio_common_msgs::AudioData_<std::allocator<void> > AudioData;

typedef boost::shared_ptr< ::audio_common_msgs::AudioData > AudioDataPtr;
typedef boost::shared_ptr< ::audio_common_msgs::AudioData const> AudioDataConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::audio_common_msgs::AudioData_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::audio_common_msgs::AudioData_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace audio_common_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'audio_common_msgs': ['/home/rhys/catkin_ws/src/audio_common/audio_common_msgs/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::audio_common_msgs::AudioData_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::audio_common_msgs::AudioData_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::audio_common_msgs::AudioData_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::audio_common_msgs::AudioData_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::audio_common_msgs::AudioData_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::audio_common_msgs::AudioData_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::audio_common_msgs::AudioData_<ContainerAllocator> >
{
  static const char* value()
  {
    return "f43a8e1b362b75baa741461b46adc7e0";
  }

  static const char* value(const ::audio_common_msgs::AudioData_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xf43a8e1b362b75baULL;
  static const uint64_t static_value2 = 0xa741461b46adc7e0ULL;
};

template<class ContainerAllocator>
struct DataType< ::audio_common_msgs::AudioData_<ContainerAllocator> >
{
  static const char* value()
  {
    return "audio_common_msgs/AudioData";
  }

  static const char* value(const ::audio_common_msgs::AudioData_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::audio_common_msgs::AudioData_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8[] data\n\
";
  }

  static const char* value(const ::audio_common_msgs::AudioData_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::audio_common_msgs::AudioData_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.data);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct AudioData_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::audio_common_msgs::AudioData_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::audio_common_msgs::AudioData_<ContainerAllocator>& v)
  {
    s << indent << "data[]" << std::endl;
    for (size_t i = 0; i < v.data.size(); ++i)
    {
      s << indent << "  data[" << i << "]: ";
      Printer<uint8_t>::stream(s, indent + "  ", v.data[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // AUDIO_COMMON_MSGS_MESSAGE_AUDIODATA_H
