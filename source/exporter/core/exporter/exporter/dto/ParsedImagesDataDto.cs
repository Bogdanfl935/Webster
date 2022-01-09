using Newtonsoft.Json;

namespace exporter.dto
{
    public class ParsedImagesDataDto
    {
        [JsonProperty("content")]
        public string content { get; set; }
        [JsonProperty("id")]
        public int id { get; set; }
        [JsonProperty("extension")]
        public string extension { get; set; }
        [JsonProperty("source")]
        public string source { get; set; }
    }
}
