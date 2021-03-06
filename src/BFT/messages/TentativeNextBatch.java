// $Id: TentativeNextBatch.java 722 2011-07-04 09:24:35Z aclement $

package BFT.messages;

import BFT.Parameters;
import util.UnsignedTypes;

/**
 * TentativeNextBatch message sent from the order node to the execution node
 * indicating the batch to be executed at sequence number n in view
 * view with history h using specified non determinism and possibly
 * taking a checkpoint after executing all requests in the batch.
 **/
public class TentativeNextBatch extends NextBatch {

    public TentativeNextBatch(Parameters param, long view, NextBatch nb) {
        this(param, view, nb.getSeqNo(), nb.getHistory(), nb.getCommands(),
                nb.getNonDeterminism(), nb.getCPDigest(), nb.takeCP(), nb.getSendingReplica());
    }

    public TentativeNextBatch(Parameters param, long view, long seq,
                              HistoryDigest hist,
                              CommandBatch batch, NonDeterminism non,
                              Digest cpDig,
                              boolean cp, long sendingReplica) {
        super(param, BFT.messages.MessageTags.TentativeNextBatch,
                view, seq, hist, batch, non, cpDig, cp, sendingReplica);
    }

    public TentativeNextBatch(Parameters param, long view, long seq, CertificateEntry entry,
                              boolean cp, long sendingReplica) {
        super(param, BFT.messages.MessageTags.TentativeNextBatch,
                view, seq, entry, cp, sendingReplica);
    }


    public TentativeNextBatch(byte[] bits, Parameters param) {
        super(bits, param);
        if (getTag() != MessageTags.TentativeNextBatch) {
            throw new RuntimeException("invalid message Tag: " + getTag());
        }
    }


    public static void main(String args[]) {
        Entry[] entries = new Entry[1];
        byte[] tmp = new byte[2];
        tmp[0] = 1;
        tmp[1] = 23;
        Parameters param = new Parameters();
        entries[0] = new Entry(param, 1234, 0, 632, tmp);
        HistoryDigest hist = new HistoryDigest(param, tmp);
        CommandBatch batch = new CommandBatch(entries);
        NonDeterminism non = new NonDeterminism(12341, 123456);

        TentativeNextBatch vmb = new TentativeNextBatch(param, 43, 234, hist, batch, non, hist, false, 3);
        //System.out.println("initial: "+vmb.toString());
        UnsignedTypes.printBytes(vmb.getBytes());
        TentativeNextBatch vmb2 = new TentativeNextBatch(vmb.getBytes(), param);
        //System.out.println("\nsecondary: "+vmb2.toString());
        UnsignedTypes.printBytes(vmb2.getBytes());

        vmb = new TentativeNextBatch(param, 134, 8, hist, batch, non, hist, true, 1);
        //System.out.println("initial: "+vmb.toString());
        UnsignedTypes.printBytes(vmb.getBytes());
        vmb2 = new TentativeNextBatch(vmb.getBytes(), param);
        //System.out.println("\nsecondary: "+vmb2.toString());
        UnsignedTypes.printBytes(vmb2.getBytes());

        //System.out.println("\nold = new: "+vmb.equals(vmb2));
    }
}
