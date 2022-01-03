namespace exporter.dto
{
    public class ExporterContentDto
    {
        public long numberNextUrls { get; set; }
        public long numberVisitedUrls { get; set; }
        public ExporterContentDto(long numberNextUrls, long numberVisitedUrls)
        {
            this.numberNextUrls = numberNextUrls;
            this.numberVisitedUrls = numberVisitedUrls;
        }
    }
}
