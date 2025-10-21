namespace api.Models;

public class LoginDetails
{
    public required string Url { get; init; } = string.Empty;
    public required CommunicationDetails Communication { get; init; }
}