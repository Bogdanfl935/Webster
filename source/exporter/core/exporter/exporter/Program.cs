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

app.MapGet("/export-content", (string username) =>
{
    var contentExporter = new ParsedContentService();
    return contentExporter.ExportContent(username);
})
    .WithName("GetExportContent");

app.MapGet("/export-images", (string username) =>
{
    var imageExporter = new ParsedImagesService();
    return imageExporter.ExportImages(username);
})
    .WithName("GetExportImages");


app.Run();
