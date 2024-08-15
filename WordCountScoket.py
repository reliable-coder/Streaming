from pyspark import SparkContext

def word_count(host, port):
  """Performs word count on data from a socket using RDDs.

  Args:
    host: Hostname of the socket (localhost).
    port: Port number of the socket(9999).
  """
  sc = SparkContext("local[*]", "SampleSocketWordCount")

  # Create a DStream from the socket
  lines = sc.textFileStream(f"tcp://{host}:{port}")

  # Flat map to create (word, 1) pairs
  words = lines.flatMap(lambda line: line.split(" "))

  # Map to create (word, 1) pairs
  word_and_one = words.map(lambda word: (word, 1))

  # Reduce by key to sum occurrences
  counts = word_and_one.reduceByKey(lambda a, b: a + b)

  # Print the results
  counts.foreachRDD(lambda rdd: rdd.foreach(print))

  counts.pprint()

if __name__ == "__main__":
  host = "localhost"
  port = 9999
  word_count(host, port)