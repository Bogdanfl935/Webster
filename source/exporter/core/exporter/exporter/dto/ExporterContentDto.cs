namespace exporter.dto
{
    public class ExporterContentDto
    {
        public Dictionary<string, string> encodedFile { get; set; }
        public ExporterContentDto(Microsoft.AspNetCore.Mvc.FileContentResult fileRez)
        {
            //this.encodedFile = System.Text.Encoding.UTF8.GetString(fileArray, 0, fileArray.Length);
            byte[] fileContent = fileRez.FileContents;
            string base64Encoded = Convert.ToBase64String(fileContent);
            this.encodedFile = new Dictionary<string, string>();
            this.encodedFile.Add("parsedContent", base64Encoded);
        }
    }
}
