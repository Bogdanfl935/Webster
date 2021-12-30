namespace exporter.dto
{
    public class ExporterImagesDto
    {
        public long numberNextUrls { get; set; }
        public long numberVisitedUrls { get; set; }
        public ExporterImagesDto(long numberNextUrls, long numberVisitedUrls)
        {
            this.numberNextUrls = numberNextUrls;
            this.numberVisitedUrls = numberVisitedUrls;
        }
    }
}
