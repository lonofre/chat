using System.Text.Json.Serialization;
using api.Models;
using Google.Protobuf.WellKnownTypes;
using Grpc.Net.Client;

var  myAllowSpecificOrigins = "_myAllowSpecificOrigins";

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Logging.AddConsole();
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.TypeInfoResolverChain.Insert(0, AppJsonSerializerContext.Default);
});

builder.Services.AddCors(options =>
{
    options.AddPolicy(name: myAllowSpecificOrigins,
        policy  =>
        {
            // Frontend address
            // Just to point out, somethin like: http://localhost:5173/ will trigger
            // a CORS error. So, delete the slash at the end
            policy.WithOrigins("http://localhost:5173")
                .AllowAnyMethod()
                .AllowAnyHeader();
        });
});

var app = builder.Build();

AppContext.SetSwitch(
    "System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);

var userChannel = GrpcChannel.ForAddress("http://localhost:50051");
var userClient = new User.UserClient(userChannel);
var messagingChannel = GrpcChannel.ForAddress("http://localhost:50052");
var messagingClient = new Messaging.MessagingClient(messagingChannel);

var api = app.MapGroup("/");

// The documentation says you must follow an order for
// adding middlewares, like CORS
app.UseCors(myAllowSpecificOrigins);

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
    var username = message.From;
    messagingClient.Send(new UserMessage() { Content = content, User = username });
    return Results.Ok(); 
});

api.MapPost("/negotiate", async (NegotiationRequest negotiation) =>
{
    var username = negotiation.Name;
    var findResponse = userClient.Find(new UserRequest { Name = username });
    if (findResponse.UserExists)
    {
        var response = await messagingClient.GetConnectionUrlAsync(new Empty());
        return Results.Ok(response);
    }
    return Results.BadRequest("User not found");
});

app.Run();

[JsonSerializable(typeof(RegisterUserRequest))]
[JsonSerializable(typeof(UserMessageRequest))]
[JsonSerializable(typeof(UrlResponse))]
[JsonSerializable(typeof(NegotiationRequest))]
internal partial class AppJsonSerializerContext : JsonSerializerContext
{
}
