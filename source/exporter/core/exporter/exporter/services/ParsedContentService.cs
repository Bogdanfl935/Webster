namespace exporter.services
{
    using RestSharp;
    using exporter.constants;
    using exporter.dto;
    using System.Text;
    using Newtonsoft.Json;
    using System.Drawing;
    using System.IO;
    using System.Net;
    using System.Drawing.Imaging;
    using System.IO.Compression;
    public class ParsedContentService
    {

        internal void ExportContent(string username)
        { 
            var nonce = 0;

            var client = new RestClient(AppConstants.appURL + ":" + EndpointConstants.storagePort);


            var requestParsedContent = new RestRequest(EndpointConstants.parsedContentEndpoint, Method.GET);
            requestParsedContent.OnBeforeDeserialization = resp => { resp.ContentType = "application/json"; };
            var responseParsedContent = client.Execute(requestParsedContent);
            var contentParsedContent = responseParsedContent.Content;

            List<Dictionary<string, string>>? listOfDict = JsonConvert.DeserializeObject<List<Dictionary<string, string>>>(contentParsedContent);

            if (listOfDict != null)
            {
                foreach (var dict in listOfDict)
                {
                    string filename;

                    byte[] valueByte = Convert.FromBase64String(dict[StorageResponseConstants.contentKey]);

                    using (MemoryStream ms = new MemoryStream(valueByte))
                    {
                        using (FileStream zipFile = File.Open(username + "_content.zip", FileMode.OpenOrCreate))
                        {
                            filename = "content_" + nonce.ToString();
                            nonce++;

                            using (ZipArchive archive = new ZipArchive(zipFile, ZipArchiveMode.Update))
                            {
                                ZipArchiveEntry readmeEntry = archive.CreateEntry(filename);

                                using (var entryStream = readmeEntry.Open())
                                using (var streamWriter = new StreamWriter(entryStream))
                                {
                                    streamWriter.Write(ms);

                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

