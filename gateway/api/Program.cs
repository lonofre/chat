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
            // Just to point out, something like: http://localhost:5173/ will trigger
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

// Registers a new user in the system. It is intended to run once per user creation.
api.MapPost("/register", (ChatUser registerRequest) =>
{
    var username = registerRequest.Name; 
    var password = registerRequest.Password;
    var findResponse = userClient.Find(new UserExistsRequest { Name = username });
    if (findResponse.UserExists)
    {
        return Results.BadRequest("User already exists");
    }
    var createResponse = userClient.Create(new UserRequest { Name = username, Password = password});
    return createResponse.Success ? Results.Ok("User registered") : Results.BadRequest("Could not register user");
});

// Send a message to the chat.
api.MapPost("/message", (Message message) =>
{
    var content = message.Content;
    var username = message.From;
    messagingClient.Send(new UserMessage() { Content = content, User = username });
    return Results.Ok(); 
});

// Login and returns additional information if the login was successful
api.MapPost("/login", (ChatUser user) =>
{
    var username = user.Name;
    var password = user.Password;
    
    var response = userClient.ValidateCredentials(new UserRequest{ Name = username, Password = password });

    if (!response.Success)
    {
        return Results.BadRequest("Invalid credentials");
    }
    
    // After a successful login, the app can return additional info to the user.
    var connectionData = messagingClient.GetConnectionUrl(new Empty());
    var loginDetails = new LoginDetails(){url = connectionData.Url};
    
    return Results.Ok(loginDetails);
    
});

app.Run();

[JsonSerializable(typeof(ChatUser))]
[JsonSerializable(typeof(Message))]
[JsonSerializable(typeof(UrlResponse))]
[JsonSerializable(typeof(NegotiationRequest))]
internal partial class AppJsonSerializerContext : JsonSerializerContext
{
}
