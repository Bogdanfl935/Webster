namespace exporter.dto
{
    public class ExporterContentDto
    {
        public byte[] encodedFile { get; set; }
        public ExporterContentDto(Microsoft.AspNetCore.Mvc.FileContentResult fileRez)
        {
            //this.encodedFile = System.Text.Encoding.UTF8.GetString(fileArray, 0, fileArray.Length);
            this.encodedFile = fileRez.FileContents;
        }
    }
}
