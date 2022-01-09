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
    using Microsoft.AspNetCore.Mvc;

    public class ParsedContentService
    {

        //internal Microsoft.AspNetCore.Mvc.FileContentResult ExportContent(string username)
        internal byte[] ExportContent(string username, string url)
        {
            var nonce = 0;

            var client = new RestClient("http://" + Environment.GetEnvironmentVariable("STORAGE_CONTAINER_NAME") + ":" + EndpointConstants.storagePort);
            //var client = new RestClient("http://127.0.0.1:" + EndpointConstants.storagePort);


            var requestParsedContent = new RestRequest(EndpointConstants.parsedContentEndpoint, Method.GET);
            requestParsedContent.AddParameter("username", username);
            requestParsedContent.AddParameter("url", url);
            requestParsedContent.OnBeforeDeserialization = resp => { resp.ContentType = "application/json"; };
            var responseParsedContent = client.Execute(requestParsedContent);
            var contentParsedContent = responseParsedContent.Content;

            ParsedContentDto parsedContent = (ParsedContentDto)JsonConvert.DeserializeObject(contentParsedContent, typeof(ParsedContentDto));
            List<ParsedContentDataDto> listOfParsedData = parsedContent.parsedContent;

            string archiveName = username + "_content.zip";

            if (listOfParsedData != null && listOfParsedData.Count > 0)
            {
                for (var i = 0;i < Math.Min(listOfParsedData.Count, 15); i ++)
                {
                    var element = listOfParsedData[i];
                    string filename;

                    byte[] valueByte = Convert.FromBase64String(element.content);


                    using (MemoryStream ms = new MemoryStream(valueByte))
                    {
                        using (FileStream zipFile = File.Open(archiveName, FileMode.OpenOrCreate))
                        {
                            filename = element.tag + "_" + element.id + ".txt";

                            using (ZipArchive archive = new ZipArchive(zipFile, ZipArchiveMode.Update))
                            {
                                string source = element.source.Replace("/", "-");
                                ZipArchiveEntry readmeEntry = archive.CreateEntry(source + "/" + element.tag + "/" + filename);

                                using (var entryStream = readmeEntry.Open())
                                using (var streamWriter = new StreamWriter(entryStream, Encoding.UTF8))
                                {
                                    streamWriter.BaseStream.Write(valueByte, 0, valueByte.Length);
                                }
                            }
                        }
                    }
                }
            }
            var myfile = System.IO.File.ReadAllBytes(archiveName);
            return new ExporterContentDto(new FileContentResult(myfile, "application/zip")).encodedFile;
            //return new ExporterContentDto(myfile).encodedFile;
        }
    }
}

