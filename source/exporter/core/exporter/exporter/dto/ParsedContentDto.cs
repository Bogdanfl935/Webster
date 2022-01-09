using Newtonsoft.Json;
namespace exporter.dto
{
    public class ParsedContentDto
    {
        [JsonProperty("parsedContent")]
        public List<ParsedContentDataDto> parsedContent { get; set; }
    }
}
