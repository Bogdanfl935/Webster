using Newtonsoft.Json;

namespace exporter.dto
{
    public class ParsedContentDataDto
    {
        [JsonProperty("content")]
        public string content { get; set; }
        [JsonProperty("id")]
        public int id { get; set; }
        [JsonProperty("tag")]
        public string tag { get; set; }
        [JsonProperty("source")]
        public string source { get; set; }
    }
}
