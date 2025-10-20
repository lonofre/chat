namespace api.Models;

public class ChatUser
{
    public required string Name { get; init; } = string.Empty;
    public required string Password { get; init; } = string.Empty;
}