using Newtonsoft.Json;
namespace exporter.dto
{
    public class ParsedImagesDto
    {
        [JsonProperty("parsedImages")]
        public List<ParsedImagesDataDto> parsedImages { get; set; }
    }
}
