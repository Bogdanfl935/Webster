using Newtonsoft.Json;

namespace exporter.dto
{
    public class ExportedContentDto
    {
        [JsonProperty("parsedContent")]
        public List<ParsedContentDataDto> parsedContent { get; set; }
    }
}
