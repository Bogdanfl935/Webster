namespace statistics.services
{
    using RestSharp;
    using statistics.constants;
    using statistics.dto;

    public class UnknownUserService
    {

        internal StatisticsDto GetStatistics()
        {
            var client = new RestClient(AppConstants.appURL + ":" + EndpointConstants.storagePort);


            var requestNextUrls = new RestRequest(EndpointConstants.numberNextUrlsEndpoint);
            var responseNextUrls = client.Get(requestNextUrls);
            var contentNextUrls = responseNextUrls.Content;

            var requestVisitedUrls = new RestRequest(EndpointConstants.numberVisitedUrlsEndpoint);
            var responseVisitedUrls = client.Get(requestVisitedUrls);
            var contentVisitedUrls = responseVisitedUrls.Content;

            var results = new StatisticsDto(long.Parse(contentNextUrls), long.Parse(contentVisitedUrls));

            return results;
        }
    }
}
