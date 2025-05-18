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

var userChannel = GrpcChannel.ForAddress("http://localhost:50051");
var userClient = new User.UserClient(userChannel);
var messagingChannel = GrpcChannel.ForAddress("http://localhost:50052");
var messagingClient = new Messaging.MessagingClient(messagingChannel);

var api = app.MapGroup("/");
api.MapGet("/", () => "Hello World!");
api.MapPost("/register", (RegisterUserRequest registerRequest) =>
{
    var username = registerRequest.Name; 
    var findResponse = userClient.Find(new UserRequest { Name = username });
    if (findResponse.UserExists)
    {
        return Results.BadRequest("User already exists");
    }
    var createResponse = userClient.Create(new UserRequest { Name = username });
    return createResponse.Success ? Results.Ok("User registered") : Results.BadRequest("Could not register user");
});

api.MapPost("/message", (UserMessageRequest message) =>
{
    var content = message.Content;
    messagingClient.Send(new UserMessage() { Content = content });
    return Results.Ok(); 
});

app.Run();

[JsonSerializable(typeof(RegisterUserRequest))]
[JsonSerializable(typeof(UserMessageRequest))]
internal partial class AppJsonSerializerContext : JsonSerializerContext
{
}
