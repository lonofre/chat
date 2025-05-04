using System.Text.Json.Serialization;
using api.Models;
using Grpc.Net.Client;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Logging.AddConsole();
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.TypeInfoResolverChain.Insert(0, AppJsonSerializerContext.Default);
});

var app = builder.Build();

AppContext.SetSwitch(
    "System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);

var channel = GrpcChannel.ForAddress("http://localhost:50051");
var client = new User.UserClient(channel);

var userApi = app.MapGroup("/");
userApi.MapGet("/", () => "Hello World!");
userApi.MapPost("/register", (RegisterUserRequest registerRequest) =>
{
    var username = registerRequest.Name; 
    var findResponse = client.Find(new UserRequest { Name = username });
    if (findResponse.UserExists)
    {
        return Results.BadRequest("User already exists");
    }
    var createResponse = client.Create(new UserRequest { Name = username });
    if (createResponse.Success)
    {
        return Results.Ok("User registered");
    }
    return Results.BadRequest("Could not register user");
});

app.Run();

[JsonSerializable(typeof(RegisterUserRequest))]
internal partial class AppJsonSerializerContext : JsonSerializerContext
{
}
