namespace statistics.dto
{
    public class StatisticsDto
    {
        public long numberNextUrls { get; set; }
        public long numberVisitedUrls { get; set; }
        public StatisticsDto(long numberNextUrls, long numberVisitedUrls)
        {
            this.numberNextUrls = numberNextUrls;
            this.numberVisitedUrls = numberVisitedUrls;
        }
    }
}
