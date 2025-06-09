namespace api.Models;

public class UserMessageRequest
{
    public required string Content { get; init; } = string.Empty;
    public required string From { get; init; } = string.Empty;
}