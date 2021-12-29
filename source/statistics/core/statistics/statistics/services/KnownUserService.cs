﻿namespace statistics.services
{
    using statistics.constants;
    using RestSharp;
    public class KnownUserService
    {

        internal Dictionary<string, string> GetStatistics(int userID)
        {
            var client = new RestClient(AppConstants.appURL + ":" + EndpointConstants.storagePort);


            var requestNextLinks = new RestRequest(EndpointConstants.numberNextLinksEndpoint);
            requestNextLinks.AddParameter("user-id", userID);
            var responseNextLinks = client.Get(requestNextLinks);
            var contentNextLinks = responseNextLinks.Content;

            var requestVisitedLinks = new RestRequest(EndpointConstants.numberVisitedLinksEndpoint);
            requestVisitedLinks.AddParameter("user-id", userID);
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
