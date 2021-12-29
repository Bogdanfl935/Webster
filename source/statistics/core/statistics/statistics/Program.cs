using statistics.services;
using statistics.constants;

using RestSharp;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.MapGet("/public-stats", () =>
{
    var publicStats = new UnknownUserService();
    return publicStats.GetStatistics();
})
    .WithName("GetPublicStatistics");

app.MapGet("/private-stats", (int userID) =>
{
    var privateStats = new KnownUserService();
    return privateStats.GetStatistics(userID);
})
    .WithName("GetPrivateStatistics");


app.Run();
