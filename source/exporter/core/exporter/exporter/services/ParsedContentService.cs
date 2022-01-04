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
            requestParsedContent.AddParameter("username", username);
            requestParsedContent.OnBeforeDeserialization = resp => { resp.ContentType = "application/json"; };
            var responseParsedContent = client.Execute(requestParsedContent);
            var contentParsedContent = responseParsedContent.Content;

            ExportedContentDto parsedContent = (ExportedContentDto)JsonConvert.DeserializeObject(contentParsedContent, typeof(ExportedContentDto));
            List<ParsedContentDataDto> listOfParsedData = parsedContent.parsedContent;

            if (listOfParsedData != null)
            {
                foreach (var element in listOfParsedData)
                {
                    string filename;

                    byte[] valueByte = Convert.FromBase64String(element.content);

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

