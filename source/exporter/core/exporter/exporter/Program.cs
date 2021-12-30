using exporter.services;

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

app.MapGet("/export-content", (int userID) =>
{
    var contentExporter = new ParsedContentService();
})
    .WithName("GetExportContent");

app.MapGet("/export-images", (int userID) =>
{
    var imageExporter = new ParsedImagesService();
    imageExporter.ExportImages(userID);
})
    .WithName("GetExportImages");


app.Run();
