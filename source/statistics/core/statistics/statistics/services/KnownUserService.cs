namespace statistics.services
{
    using statistics.constants;
    using RestSharp;
    using statistics.dto;
    public class KnownUserService
    {

        internal StatisticsDto GetStatistics(int userID)
        {
            var client = new RestClient(AppConstants.appURL + ":" + EndpointConstants.storagePort);


            var requestNextUrls = new RestRequest(EndpointConstants.numberNextUrlsEndpoint);
            requestNextUrls.AddParameter("user-id", userID);
            var responseNextUrls = client.Get(requestNextUrls);
            var contentNextUrls = responseNextUrls.Content;

            var requestVisitedUrls = new RestRequest(EndpointConstants.numberVisitedUrlsEndpoint);
            requestVisitedUrls.AddParameter("user-id", userID);
            var responseVisitedUrls = client.Get(requestVisitedUrls);
            var contentVisitedUrls = responseVisitedUrls.Content;

            var results = new StatisticsDto(long.Parse(contentNextUrls), long.Parse(contentVisitedUrls));

            return results;
        }
    }
}
