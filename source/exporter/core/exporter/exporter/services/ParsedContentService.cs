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

        internal void ExportContent(int userID)
        {
            var dictExtensions = new Dictionary<string, ImageFormat>()
            {
                {"jpeg", ImageFormat.Jpeg},
                {"jpg", ImageFormat.Jpeg },
                {"png", ImageFormat.Png},
                {"gif", ImageFormat.Gif},
                {"bmp", ImageFormat.Bmp},
                {"ico", ImageFormat.Icon},
                {"exif", ImageFormat.Exif},
                {"tiff", ImageFormat.Tiff},
                {"wmf", ImageFormat.Wmf},
            };

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

                        filename = System.Convert.ToBase64String(Encoding.UTF8.GetBytes((nonce.ToString() + userID.ToString()).ToCharArray())) + userID;
                        using (FileStream file = new FileStream(filename, FileMode.Create, FileAccess.Write))
                        {
                            ms.WriteTo(file);
                        }
                        nonce++;
                    }

                    using (FileStream zipFile = File.Open(userID + "_content.zip", FileMode.OpenOrCreate))
                    {
                        using (ZipArchive archive = new ZipArchive(zipFile, ZipArchiveMode.Update))
                        {
                            ZipArchiveEntry readmeEntry = archive.CreateEntry(filename);

                            archive.CreateEntry(filename);
                        }
                    }
                }
            }
        }
    }
}

