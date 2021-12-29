namespace statistics.services
{
    using statistics.constants;
    using RestSharp;
    public class UnknownUserService
    {

        internal Dictionary<string, string> GetStatistics()
        {
            var client = new RestClient(AppConstants.appURL + ":" + EndpointConstants.storagePort);


            var requestNextLinks = new RestRequest(EndpointConstants.numberNextLinksEndpoint);
            var responseNextLinks = client.Get(requestNextLinks);
            var contentNextLinks = responseNextLinks.Content;

            var requestVisitedLinks = new RestRequest(EndpointConstants.numberVisitedLinksEndpoint);
            var responseVisitedLinks = client.Get(requestVisitedLinks);
            var contentVisitedLinks = responseVisitedLinks.Content;

            var results = new Dictionary<string, string>
            {
                {"numberNextLinks", contentNextLinks },
                {"numberVisitedLinks", contentVisitedLinks }
            };

            return results;
        }
    }
}
