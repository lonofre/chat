namespace api.utils;

using Google.Protobuf.WellKnownTypes;
using System.Collections.Generic;
using System.Linq;

public static class ProtoStructExtensions
{
    /// <summary>
    /// Converts the Proto Struct to a dictionary, so getting the values is easier.
    /// </summary>
    /// <param name="protoStruct">A struct that contains object-data</param>
    /// <returns>A dictionary that could contain the values (if it is possible to parse)</returns>
    public static Dictionary<string, object?> ToDictionary(this Struct protoStruct)
    {
        return protoStruct.Fields.ToDictionary(
            kvp => kvp.Key,
            kvp => ConvertValue(kvp.Value)
        );
    }

    private static object? ConvertValue(Value value)
    {
        switch (value.KindCase)
        {
            case Value.KindOneofCase.BoolValue:
                return value.BoolValue;
            case Value.KindOneofCase.NumberValue:
                return value.NumberValue;
            case Value.KindOneofCase.StringValue:
                return value.StringValue;
            case Value.KindOneofCase.StructValue:
                return value.StructValue.ToDictionary();
            case Value.KindOneofCase.ListValue:
                return value.ListValue.Values.Select(ConvertValue).ToList();
            case Value.KindOneofCase.NullValue:
            default:
                return null;
        }
    }
    
    
}